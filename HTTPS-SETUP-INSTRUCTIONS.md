# 🔒 HTTPS Setup with Let's Encrypt (Free & Auto-Renewal)

## Quick Setup (5 minutes)

### Prerequisites
1. **Domain name** pointing to your server IP (`159.89.161.170`)
2. **SSH access** to the server
3. **Root/sudo access**

### Step 1: Point Domain to Server

Add an **A record** in your domain's DNS:
```
Type: A
Name: api (or @ for root domain)
Value: 159.89.161.170
TTL: 300 (or default)
```

**Examples:**
- `api.nadidosh.com` → `159.89.161.170`
- `nadidosh.com` → `159.89.161.170`
- `api.yourdomain.com` → `159.89.161.170`

Wait 5-10 minutes for DNS to propagate, then verify:
```bash
ping api.yourdomain.com
# Should show: 159.89.161.170
```

### Step 2: Run Setup Script

```bash
# Copy script to server
scp -i deploy_key -P 22 setup-https-auto-renew.sh root@159.89.161.170:/root/

# SSH to server
ssh -i deploy_key -p 22 root@159.89.161.170

# Run setup script
bash setup-https-auto-renew.sh
```

The script will:
1. ✅ Install Nginx and Certbot
2. ✅ Configure Nginx as reverse proxy
3. ✅ Get SSL certificate from Let's Encrypt
4. ✅ Set up automatic renewal
5. ✅ Configure security headers

### Step 3: Update Client Code

Update `script.js` line 3108:
```javascript
const PRODUCTION_API_HTTP = 'https://api.yourdomain.com'; // Your domain
```

### Step 4: Test

```bash
# Test HTTPS endpoint
curl https://api.yourdomain.com/api/health

# Should return: {"status":"healthy","service":"Nadi Dosha Calculator API"}
```

## Auto-Renewal

### How It Works
- **Certificates expire**: Every 90 days
- **Auto-renewal**: Runs daily at 3 AM
- **Nginx reload**: Automatically after renewal
- **No downtime**: Seamless renewal

### Verify Auto-Renewal

```bash
# Check certificate status
certbot certificates

# Test renewal (dry run)
certbot renew --dry-run

# View renewal logs
journalctl -u certbot.timer
```

### Manual Renewal (if needed)

```bash
certbot renew
systemctl reload nginx
```

## What Gets Installed

1. **Nginx** - Reverse proxy server
2. **Certbot** - Let's Encrypt client
3. **SSL Certificate** - Free from Let's Encrypt
4. **Auto-renewal** - Cron job + systemd timer

## Configuration Files

- **Nginx config**: `/etc/nginx/sites-available/nadi-api`
- **SSL certificates**: `/etc/letsencrypt/live/your-domain.com/`
- **Renewal config**: `/etc/letsencrypt/renewal/your-domain.com.conf`

## Troubleshooting

### Certificate Not Obtaining

1. **Check DNS**: `ping your-domain.com` should show server IP
2. **Check port 80**: `netstat -tlnp | grep :80` (should be open)
3. **Check Nginx**: `systemctl status nginx`
4. **Check logs**: `journalctl -u certbot`

### Renewal Fails

1. **Check DNS still points to server**
2. **Check port 80 is accessible**
3. **Run manual renewal**: `certbot renew --force-renewal`

### Nginx Not Starting

```bash
# Test configuration
nginx -t

# Check logs
journalctl -u nginx
```

## Security Features

The setup includes:
- ✅ HTTPS redirect (HTTP → HTTPS)
- ✅ HSTS header (force HTTPS)
- ✅ Security headers (X-Frame-Options, etc.)
- ✅ Modern SSL configuration

## Cost

- **Let's Encrypt**: 100% Free
- **Nginx**: Free (open source)
- **Certbot**: Free
- **Auto-renewal**: Free
- **Total**: $0.00

## After Setup

Your API will be accessible at:
- ✅ `https://your-domain.com/api/health`
- ✅ `https://your-domain.com/api/calculate-nadi-complete`
- ✅ `https://your-domain.com/docs` (API documentation)

**No more proxies needed!** Simple HTTP calls work directly. 🎉

