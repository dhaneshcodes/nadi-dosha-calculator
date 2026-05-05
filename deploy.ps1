# Production deployment (repo docs: api.nadidosh.com -> 159.89.161.170, path /var/www/nadi-dosha-calculator).
# Private keys are not in git. Optional: $env:NADI_SSH_KEY = 'C:\path\to\key'

$ErrorActionPreference = "Stop"
$RootDir = $PSScriptRoot

$SERVER_IP = "159.89.161.170"
$SERVER_PORT = 22
$SERVER_USER = "root"
$APP_DIR = "/var/www/nadi-dosha-calculator"
$SERVICE_NAME = "nadi-dosha-calculator"

function Resolve-NadiSshKey {
    param([string]$BaseDir)

    $candidates = @()
    if ($env:NADI_SSH_KEY) { $candidates += $env:NADI_SSH_KEY.Trim() }
    $candidates += (Join-Path $BaseDir "deploy_key")
    $homeSsh = Join-Path $env:USERPROFILE ".ssh"
    $candidates += @(
        (Join-Path $homeSsh "id_ed25519"),
        (Join-Path $homeSsh "id_rsa"),
        (Join-Path $homeSsh "nadi_deploy_key")
    )

    foreach ($path in $candidates) {
        if ([string]::IsNullOrWhiteSpace($path)) { continue }
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            return (Resolve-Path -LiteralPath $path).Path
        }
    }
    return $null
}

$SshIdentity = Resolve-NadiSshKey $RootDir

Write-Host "`nDeploying -> ${SERVER_USER}@${SERVER_IP}:${APP_DIR}" -ForegroundColor Green
Write-Host "Public API (per repo docs): https://api.nadidosh.com" -ForegroundColor DarkGray

if (-not $SshIdentity) {
    Write-Host "`nNo SSH private key found. Checked:" -ForegroundColor Red
    Write-Host "  env NADI_SSH_KEY" -ForegroundColor Yellow
    Write-Host "  $(Join-Path $RootDir 'deploy_key')" -ForegroundColor Yellow
    Write-Host "  $env:USERPROFILE\.ssh\id_ed25519 | id_rsa | nadi_deploy_key" -ForegroundColor Yellow
    Write-Host "`nExample: `$env:NADI_SSH_KEY = 'C:\path\to\droplet_key'; .\deploy.ps1" -ForegroundColor Cyan
    exit 1
}

Write-Host "Using SSH key: $SshIdentity" -ForegroundColor DarkCyan

if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) { throw "OpenSSH ssh not found in PATH." }
if (-not (Get-Command scp -ErrorAction SilentlyContinue)) { throw "OpenSSH scp not found in PATH." }

$Remote = "${SERVER_USER}@${SERVER_IP}"
$SshCommon = @("-i", $SshIdentity, "-p", "${SERVER_PORT}", "-o", "StrictHostKeyChecking=no")
function Invoke-RemoteShell {
    param([string]$Inline)
    ssh @SshCommon $Remote @("bash", "-lc", $Inline)
}

Write-Host "`nTesting SSH..." -ForegroundColor Yellow
Invoke-RemoteShell "echo ok"
if ($LASTEXITCODE -ne 0) {
    Write-Host "SSH connection failed." -ForegroundColor Red
    exit 1
}

Write-Host "SSH OK." -ForegroundColor Green
Write-Host "`nEnsuring app directory..." -ForegroundColor Yellow
Invoke-RemoteShell "mkdir -p $APP_DIR"
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`nUploading server/ ..." -ForegroundColor Yellow
Push-Location $RootDir
try {
    $scpSrv = @("-i", $SshIdentity, "-P", "${SERVER_PORT}", "-o", "StrictHostKeyChecking=no", "-r", "server", "${Remote}:${APP_DIR}/")
    scp @scpSrv
    if ($LASTEXITCODE -ne 0) { throw "scp server/ failed" }

    $staticRoots = @(
        "server.py", "requirements.txt",
        "index.html", "script.js", "styles.css", "air-datepicker-theme.css",
        "manifest.json", "sw.js", "robots.txt", "sitemap.xml", "CNAME"
    )
    $icons = @(Get-ChildItem -Path "." -Filter "icon-*.png" -ErrorAction SilentlyContinue | ForEach-Object { $_.Name })
    $paths = @()
    foreach ($f in ($staticRoots + $icons)) {
        if (Test-Path -LiteralPath $f) { $paths += $f }
    }
    if ($paths.Count -gt 0) {
        $scpFiles = @("-i", $SshIdentity, "-P", "${SERVER_PORT}", "-o", "StrictHostKeyChecking=no") + $paths + "${Remote}:${APP_DIR}/"
        scp @scpFiles
        if ($LASTEXITCODE -ne 0) { throw "scp static files failed" }
    }
} finally {
    Pop-Location
}

Write-Host "`nInstalling Python deps on server..." -ForegroundColor Yellow
$install = "cd $APP_DIR && python3 -m pip install -q --upgrade pip && python3 -m pip install -q -r requirements.txt && echo deps_ok"
Invoke-RemoteShell $install
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`nRestarting systemd: $SERVICE_NAME..." -ForegroundColor Yellow
$unit = @"
[Unit]
Description=Nadi Dosha Calculator API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 $APP_DIR/server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"@
$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($unit))
Invoke-RemoteShell "echo $b64 | base64 -d > /etc/systemd/system/$SERVICE_NAME.service && systemctl daemon-reload && systemctl enable $SERVICE_NAME && systemctl restart $SERVICE_NAME && sleep 2 && systemctl is-active --quiet $SERVICE_NAME && echo active_ok"
if ($LASTEXITCODE -ne 0) {
    Invoke-RemoteShell "systemctl status $SERVICE_NAME --no-pager || true"
    exit 1
}

Write-Host "`nDeployment finished." -ForegroundColor Green
Write-Host "Health: curl -s https://api.nadidosh.com/api/health" -ForegroundColor Cyan
