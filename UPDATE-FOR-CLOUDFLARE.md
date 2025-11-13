# ✅ Cloudflare Setup - Next Steps

## What's Done
- ✅ DNS A record: `api` → `159.89.161.170` (proxied)
- ✅ Cloudflare provides free SSL automatically
- ✅ Server updated to use port 80 (for Cloudflare)

## What We Need

**Your domain name** - What domain did you use?
- Example: If domain is `nadidosh.com`, API will be `api.nadidosh.com`
- Example: If domain is `yourdomain.com`, API will be `api.yourdomain.com`

## Once You Provide Domain Name

I'll update `script.js`:
```javascript
const PRODUCTION_API_HTTP = 'https://api.yourdomain.com'; // Your actual domain
```

## Server Update

Server is now configured to use **port 80** (Cloudflare default).

**Restart the server:**
```bash
ssh -i deploy_key -p 22 root@159.89.161.170
cd /var/www/nadi-dosha-calculator
pkill -f 'python3.*server.py'
python3 server.py > server.log 2>&1 &
```

Or if using systemd:
```bash
systemctl restart nadi-dosha-calculator
```

## Test After Restart

Wait 2-5 minutes for DNS, then:
```bash
curl https://api.yourdomain.com/api/health
```

Should return: `{"status":"healthy","service":"Nadi Dosha Calculator API"}`

## How It Works Now

```
GitHub Pages (HTTPS)
    ↓
Cloudflare (HTTPS) ← Free SSL!
    ↓
Your Server (HTTP:80) ← Changed from 8000
```

**No proxies needed!** Simple HTTP calls work directly. 🎉

