# 🔒 Setting Up HTTPS for API Server

## Quick Setup with Let's Encrypt (Free SSL)

### Step 1: Install Certbot

```bash
ssh -i deploy_key -p 22 root@159.89.161.170

# Update system
apt-get update

# Install certbot
apt-get install -y certbot python3-certbot-nginx
```

### Step 2: Get SSL Certificate

**Option A: If you have a domain pointing to the server:**

```bash
# Replace your-domain.com with your actual domain
certbot certonly --standalone -d your-domain.com
```

**Option B: If you only have IP address:**

You'll need to use a service like:
- **Cloudflare** (free SSL proxy)
- **Nginx with self-signed cert** (browser warnings)
- **CORS proxy service** (temporary)

### Step 3: Configure Nginx Reverse Proxy

```bash
# Install Nginx
apt-get install -y nginx

# Create Nginx config
cat > /etc/nginx/sites-available/nadi-api << 'EOF'
server {
    listen 80;
    server_name 159.89.161.170;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name 159.89.161.170;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/nadi-api /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 4: Update Client Code

Change `script.js`:
```javascript
const PRODUCTION_API = 'https://your-domain.com'; // or https://159.89.161.170:443
```

## Alternative: Cloudflare (Easiest - No Server Config)

1. **Add domain to Cloudflare**
2. **Point DNS to your server IP** (159.89.161.170)
3. **Enable Cloudflare proxy** (orange cloud icon)
4. **Cloudflare provides free SSL automatically**
5. **Update API URL to use your domain**

## Alternative: Use Railway/Render (Free HTTPS Proxy)

Deploy a simple proxy server on Railway or Render that:
- Accepts HTTPS
- Proxies to your HTTP API
- Adds CORS headers

## Current Status

- ❌ API: HTTP only (blocked by browsers from HTTPS pages)
- ✅ Need: HTTPS endpoint
- 💡 Best: Set up Let's Encrypt SSL certificate

## Testing

After setting up HTTPS:
1. Update `API_BASE_URL` in `script.js` to use `https://`
2. Test from GitHub Pages
3. No more mixed content errors!

