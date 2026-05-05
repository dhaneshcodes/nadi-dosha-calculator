# 🔒 Mixed Content Issue - HTTPS to HTTP

## Problem
GitHub Pages is served over **HTTPS**, but the API server is **HTTP**. Browsers block mixed content (HTTPS page loading HTTP resources) for security reasons.

**Error:** `(blocked:mixed-content)`

## Solutions

### Solution 1: Set Up HTTPS on API Server (Recommended)

This is the best long-term solution. You need an SSL certificate for your API server.

#### Option A: Use Let's Encrypt (Free SSL)

```bash
# On the server
apt-get update
apt-get install certbot python3-certbot-nginx

# If using Nginx as reverse proxy
certbot --nginx -d your-domain.com

# Or if using standalone
certbot certonly --standalone -d your-domain.com
```

Then configure your server to use HTTPS on port 443.

#### Option B: Use Cloudflare (Free SSL Proxy)

1. Add your domain to Cloudflare
2. Point DNS to your server IP
3. Enable Cloudflare proxy (orange cloud)
4. Cloudflare provides free SSL automatically

### Solution 2: Use CORS Proxy Service (Temporary)

Use a CORS proxy service that supports HTTPS:

```javascript
// In script.js, update API_BASE_URL:
const CORS_PROXY = 'https://cors-anywhere.herokuapp.com/';
const PRODUCTION_API = 'http://159.89.161.170:8000';
const baseUrl = isHTTPS ? `${CORS_PROXY}${PRODUCTION_API}` : PRODUCTION_API;
```

**Note:** Free CORS proxies have rate limits and may not be reliable for production.

### Solution 3: Use Your Own HTTPS CORS Proxy

Set up a simple HTTPS proxy server (e.g., on Heroku, Railway, or Render) that:
1. Accepts HTTPS requests
2. Proxies to your HTTP API server
3. Adds CORS headers

### Solution 4: Use Nginx Reverse Proxy with SSL

Set up Nginx on your server with SSL:

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Quick Fix (Temporary)

For immediate testing, you can:

1. **Use a CORS proxy service** (not recommended for production)
2. **Set up a free HTTPS proxy** on services like:
   - Railway.app
   - Render.com
   - Fly.io
   - Heroku

## Recommended Approach

1. **Short term:** Use a CORS proxy or set up a free HTTPS proxy service
2. **Long term:** Set up HTTPS on your API server using Let's Encrypt or Cloudflare

## Testing

After implementing HTTPS:
1. Update `API_BASE_URL` in `script.js` to use `https://` instead of `http://`
2. Test from GitHub Pages
3. Verify no mixed content errors in browser console

## Current Status

- ❌ API server: HTTP only
- ✅ GitHub Pages: HTTPS
- ❌ Mixed content: Blocked by browser

## Next Steps

1. Set up SSL certificate on API server (Let's Encrypt recommended)
2. Configure server to listen on HTTPS (port 443)
3. Update `API_BASE_URL` to use `https://159.89.161.170:443` or your domain
4. Test from GitHub Pages

