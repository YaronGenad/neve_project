#!/usr/bin/env bash
# ── init-ssl.sh ──────────────────────────────────────────────────────────────
# First-time Let's Encrypt certificate acquisition for Al-Hasade production.
#
# Run ONCE before starting the full production stack:
#   chmod +x scripts/init-ssl.sh
#   DOMAIN=yourdomain.com EMAIL=admin@yourdomain.com ./scripts/init-ssl.sh
#
# Prerequisites:
#   - DOMAIN points to this server's IP (DNS propagated)
#   - Port 80 is open
#   - Docker is installed

set -euo pipefail

DOMAIN="${DOMAIN:?Set DOMAIN=yourdomain.com}"
EMAIL="${EMAIL:?Set EMAIL=admin@yourdomain.com}"

echo "==> Acquiring SSL certificate for $DOMAIN"

# Create directory structure expected by nginx.conf and docker-compose.prod.yml
mkdir -p certbot/conf certbot/www

# Start a temporary nginx to serve the ACME challenge
docker run --rm -d \
  --name certbot-tmp-nginx \
  -p 80:80 \
  -v "$(pwd)/certbot/www:/var/www/certbot" \
  nginx:alpine sh -c "
    echo 'server { listen 80; location /.well-known/acme-challenge/ { root /var/www/certbot; } }' \
      > /etc/nginx/conf.d/default.conf
    nginx -g 'daemon off;'"

# Wait for nginx to come up
sleep 3

# Obtain the certificate
docker run --rm \
  -v "$(pwd)/certbot/conf:/etc/letsencrypt" \
  -v "$(pwd)/certbot/www:/var/www/certbot" \
  certbot/certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN"

# Stop the temporary nginx
docker stop certbot-tmp-nginx || true

echo "==> Certificate acquired! Files in certbot/conf/live/$DOMAIN/"
echo "==> Update nginx.conf: replace YOURDOMAIN.COM with $DOMAIN"
echo "==> Then start the production stack:"
echo "    docker compose -f docker-compose.prod.yml --env-file .env.prod up -d"
