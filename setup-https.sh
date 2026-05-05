#!/bin/bash
# Quick HTTPS setup script for API server

echo "🔒 Setting up HTTPS for API server..."

# Install Nginx
apt-get update
apt-get install -y nginx

# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Check if domain is configured
read -p "Do you have a domain pointing to this server? (y/n): " has_domain

if [ "$has_domain" = "y" ]; then
    read -p "Enter your domain name: " domain_name
    
    # Get SSL certificate
    certbot certonly --standalone -d $domain_name --non-interactive --agree-tos --email admin@$domain_name
    
    # Create Nginx config
    cat > /etc/nginx/sites-available/nadi-api << EOF
server {
    listen 80;
    server_name $domain_name;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $domain_name;

    ssl_certificate /etc/letsencrypt/live/$domain_name/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$domain_name/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    # Enable site
    ln -sf /etc/nginx/sites-available/nadi-api /etc/nginx/sites-enabled/
    nginx -t && systemctl restart nginx
    
    echo "✅ HTTPS configured! Use: https://$domain_name"
else
    echo "⚠️  Without a domain, you need to:"
    echo "1. Get a free domain (Freenom, etc.)"
    echo "2. Point it to this server IP: $(curl -s ifconfig.me)"
    echo "3. Run this script again"
    echo ""
    echo "Or use Cloudflare (easiest):"
    echo "1. Add domain to Cloudflare"
    echo "2. Point DNS to this server"
    echo "3. Enable Cloudflare proxy (orange cloud)"
    echo "4. Cloudflare provides free SSL automatically"
fi

