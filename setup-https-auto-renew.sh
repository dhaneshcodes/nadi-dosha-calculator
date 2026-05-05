#!/bin/bash
# Let's Encrypt HTTPS Setup with Auto-Renewal
# Run this on your server: bash setup-https-auto-renew.sh

set -e  # Exit on error

echo "🔒 Setting up HTTPS with Let's Encrypt (Free & Unlimited)"
echo "=========================================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt-get update -qq

# Install required packages
echo "📦 Installing Nginx and Certbot..."
apt-get install -y nginx certbot python3-certbot-nginx

# Get domain name
echo ""
read -p "Enter your domain name (e.g., api.nadidosh.com): " domain_name

if [ -z "$domain_name" ]; then
    echo "❌ Domain name is required"
    exit 1
fi

# Verify domain points to this server
echo ""
echo "🔍 Verifying domain points to this server..."
server_ip=$(curl -s ifconfig.me)
echo "   Server IP: $server_ip"
echo "   Domain: $domain_name"
echo ""
read -p "Does $domain_name point to $server_ip? (y/n): " domain_verified

if [ "$domain_verified" != "y" ]; then
    echo "❌ Please point your domain to this server IP first"
    echo "   Add A record: $domain_name -> $domain_name"
    exit 1
fi

# Get email for Let's Encrypt
echo ""
read -p "Enter email for Let's Encrypt notifications: " email

# Create Nginx configuration
echo ""
echo "📝 Creating Nginx configuration..."
cat > /etc/nginx/sites-available/nadi-api << EOF
# HTTP server - redirect to HTTPS
server {
    listen 80;
    server_name $domain_name;

    # Let's Encrypt verification
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name $domain_name;

    # SSL certificates (will be added by certbot)
    # ssl_certificate /etc/letsencrypt/live/$domain_name/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/$domain_name/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Proxy to Python server
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable site
echo "🔗 Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/nadi-api /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
nginx -t

# Start Nginx
echo "🚀 Starting Nginx..."
systemctl enable nginx
systemctl restart nginx

# Get SSL certificate
echo ""
echo "🔐 Obtaining SSL certificate from Let's Encrypt..."
certbot --nginx -d $domain_name --non-interactive --agree-tos --email $email --redirect

# Verify certificate
if [ -f "/etc/letsencrypt/live/$domain_name/fullchain.pem" ]; then
    echo "✅ SSL certificate installed successfully!"
else
    echo "❌ Failed to obtain certificate"
    exit 1
fi

# Set up auto-renewal
echo ""
echo "🔄 Setting up automatic renewal..."

# Create renewal hook script
cat > /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh << 'HOOK_EOF'
#!/bin/bash
# Reload Nginx after certificate renewal
systemctl reload nginx
HOOK_EOF

chmod +x /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh

# Test renewal (dry run)
echo "🧪 Testing certificate renewal..."
certbot renew --dry-run

# Add cron job for auto-renewal (certbot handles this, but verify)
if ! crontab -l 2>/dev/null | grep -q "certbot renew"; then
    echo "📅 Adding auto-renewal cron job..."
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --deploy-hook /etc/letsencrypt/renewal-hooks/deploy/nginx-reload.sh") | crontab -
fi

# Final status
echo ""
echo "=========================================================="
echo "✅ HTTPS Setup Complete!"
echo "=========================================================="
echo ""
echo "🌐 Your API is now available at:"
echo "   https://$domain_name"
echo ""
echo "📋 Next Steps:"
echo "   1. Update script.js line 3108:"
echo "      const PRODUCTION_API_HTTP = 'https://$domain_name';"
echo ""
echo "   2. Test the API:"
echo "      curl https://$domain_name/api/health"
echo ""
echo "🔄 Auto-renewal:"
echo "   - Certificates renew automatically every 90 days"
echo "   - Cron job runs daily at 3 AM"
echo "   - Nginx reloads automatically after renewal"
echo ""
echo "📊 Check certificate status:"
echo "   certbot certificates"
echo ""
echo "🔍 View renewal logs:"
echo "   journalctl -u certbot.timer"
echo ""

