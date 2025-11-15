# PowerShell Deployment Script for Nadi Dosha Calculator
# Server: 159.89.161.170:22

$SERVER_IP = "159.89.161.170"
$SERVER_USER = "root"
$SSH_KEY = "deploy_key"
$APP_DIR = "/var/www/nadi-dosha-calculator"
$SERVICE_NAME = "nadi-dosha-calculator"

Write-Host "🚀 Starting deployment to $SERVER_IP..." -ForegroundColor Green

# Step 1: Test SSH connection
Write-Host "`n📡 Testing SSH connection..." -ForegroundColor Yellow
try {
    $testResult = ssh -i $SSH_KEY -o StrictHostKeyChecking=no -p 22 "$SERVER_USER@$SERVER_IP" "echo 'Connection successful!'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Connection successful!" -ForegroundColor Green
    } else {
        Write-Host "❌ Connection failed!" -ForegroundColor Red
        Write-Host $testResult
        exit 1
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Create app directory
Write-Host "`n📁 Creating app directory..." -ForegroundColor Yellow
ssh -i $SSH_KEY -p 22 "$SERVER_USER@$SERVER_IP" "mkdir -p $APP_DIR"

# Step 3: Transfer files
Write-Host "`n📦 Transferring files..." -ForegroundColor Yellow
Write-Host "   Transferring server directory..." -ForegroundColor Gray
scp -i $SSH_KEY -P 22 -r server "$SERVER_USER@${SERVER_IP}:$APP_DIR/" 2>&1 | Out-Null

Write-Host "   Transferring main files..." -ForegroundColor Gray
scp -i $SSH_KEY -P 22 server.py requirements.txt index.html script.js styles.css air-datepicker-theme.css "$SERVER_USER@${SERVER_IP}:$APP_DIR/" 2>&1 | Out-Null

# Step 4: Install Python dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
$installScript = @"
cd $APP_DIR
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet
echo 'Dependencies installed'
"@

ssh -i $SSH_KEY -p 22 "$SERVER_USER@$SERVER_IP" $installScript

# Step 5: Create systemd service
Write-Host "`n⚙️  Creating systemd service..." -ForegroundColor Yellow
$serviceScript = @"
cat > /etc/systemd/system/$SERVICE_NAME.service << 'EOFSERVICE'
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
EOFSERVICE

systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl restart $SERVICE_NAME
sleep 2
systemctl status $SERVICE_NAME --no-pager
"@

ssh -i $SSH_KEY -p 22 "$SERVER_USER@$SERVER_IP" $serviceScript

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Server should be running on http://$SERVER_IP:8000" -ForegroundColor Cyan
