# Zengeza Rentals

A Django-based rental management system for landlords and tenants in Zimbabwe.

## Features

- **Role-based user management** (Admin, Landlord, Tenant)
- **Property listings** with photo uploads and search functionality
- **Secure payment processing** with mobile money integration (EcoCash, InnBucks, OneMoney)
- **72-hour payment unlock system** for contact details
- **Admin dashboard** for property and payment approvals
- **Landlord dashboard** for property management
- **Tenant dashboard** for payment tracking and active unlocks
- **User registration and authentication**
- **Responsive design** with modern UI

## Quick Start

### Development Setup

1. **Clone and setup virtual environment:**
   ```bash
   git clone <repository-url>
   cd zengeza_rentals
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - **Home Page**: http://127.0.0.1:8000/
   - **Property Listings**: http://127.0.0.1:8000/properties/
   - **Login/Register**: http://127.0.0.1:8000/login/ | http://127.0.0.1:8000/register/
   - **Dashboards**: Based on user role after login
   - **Admin Panel**: http://127.0.0.1:8000/admin/

### Sample Test Accounts

- **Admin**: username: `admin`, password: `admin123`
- **Landlord**: username: `landlord1`, password: `pass123`
- **Tenant**: username: `tenant1`, password: `pass123`
- **Sample Property**: "Sample Apartment" (ID: 1) at http://127.0.0.1:8000/property/1/

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production setup instructions.

## Project Structure

```
zengeza_rentals/
│
├── zengeza_rentals/      # Django project folder
│   ├── __init__.py
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URLs
│   ├── wsgi.py
│   └── asgi.py
│
├── rentals/              # Django app
│   ├── migrations/
│   ├── templates/
│   │   └── rentals/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── property_list.html
│   │       ├── property_detail.html
│   │       ├── add_property.html
│   │       ├── submit_payment.html
│   │       ├── tenant_dashboard.html
│   │       ├── landlord_dashboard.html
│   │       └── admin_dashboard.html
│   ├── static/
│   │   └── rentals/
│   │       └── css/ (optional custom styles)
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── decorators.py
│
├── manage.py
├── requirements.txt
├── db.sqlite3
├── media/                # User uploaded files
├── staticfiles/          # Collected static files
└── logs/                 # Application logs
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
DJANGO_SECRET_KEY=your-secret-key
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
ALLOWED_HOSTS=yourdomain.com
```

## Security Features

- CSRF protection
- Secure password hashing
- Role-based access control
- HTTPS enforcement in production
- Secure cookie settings
- Content security headers

## Technologies Used

- Django 5.2.9
- PostgreSQL (production) / SQLite (development)
- Pillow (image processing)
- WhiteNoise (static files)
- Gunicorn (WSGI server)

## License

This project is licensed under the MIT License.