# Zengeza Rentals - Production Deployment Guide

## 🚀 Production Setup

### 1. Environment Variables
Set these environment variables on your production server:

```bash
# Django Settings
export DJANGO_SETTINGS_MODULE=zengeza_rentals.settings_production
export DJANGO_SECRET_KEY="your-secure-secret-key-here"

# Database (PostgreSQL recommended for production)
export DB_NAME="zengeza_rentals_prod"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"
export DB_HOST="localhost"
export DB_PORT="5432"

# Email Settings
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-app-password"
```

### 2. Install Production Dependencies
```bash
pip install gunicorn psycopg2-binary whitenoise
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb zengetza_rentals_prod

# Run migrations
python manage.py migrate
```

### 4. Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 5. Gunicorn Setup
Create a systemd service file `/etc/systemd/system/zengeza-rentals.service`:

```ini
[Unit]
Description=Zengeza Rentals Django App
After=network.target

[Service]
User=your-user
Group=your-group
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=zengeza_rentals.settings_production"
ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 zengeza_rentals.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 6. Nginx Configuration
Create `/etc/nginx/sites-available/zengeza-rentals`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### 7. SSL Certificate (Let's Encrypt)
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 8. Start Services
```bash
# Enable and start services
sudo systemctl enable zengetza-rentals
sudo systemctl start zengetza-rentals
sudo systemctl enable nginx
sudo systemctl restart nginx
```

## 🔒 Security Checklist
- [ ] DEBUG = False
- [ ] Secure SECRET_KEY set
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Database credentials in environment variables
- [ ] Regular backups configured
- [ ] Firewall configured
- [ ] Updates applied regularly

## 📊 Monitoring
Consider setting up:
- Error logging and monitoring
- Performance monitoring
- Backup automation
- Security updates

## 🆘 Troubleshooting
- Check Django logs: `journalctl -u zengetza-rentals`
- Check Nginx logs: `tail -f /var/log/nginx/error.log`
- Test database connection: `python manage.py dbshell`