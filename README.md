
# Ecommerce Django Application

A modular ecommerce application built using Django, MySQL, Django REST Framework, JWT authentication, and Stripe payments. The system runs in a Python virtual environment and uses PyMySQL to connect to MySQL on macOS.

## 1. Project Overview

This project includes:

- User authentication with Django & JWT
- Admin portal for inventory and user management
- Product catalog and cart processing
- Stripe-based payment flow
- Static & media file handling
- MySQL storage using PyMySQL

Project Modules:
```
ecommerce/
│
├─ ecommerce/              # Main project (settings, URLs, WSGI)
│
├─ users/                  # Authentication and profile related logic
│
├─ store/                  # Products, catalog, static assets
│
├─ checkout/               # Cart, Stripe integration, order capture
│
├─ requirements.txt        # Dependency pinning
│
└─ manage.py

```

## 2. System Requirements

- Python 3.11+
- macOS or windows
- MySQL Community Server (DMG installation) for MacOS
- MySQL Installer for Windows
- pip / virtualenv

## 3. Python Dependencies

```
Django==5.1.1
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
PyMySQL==1.1.1
stripe==10.0.0
pillow
requests
```

## 4. Environment Setup

Clone the repository and move into the project:

```
git clone <https://github.com/KRISHNAREDDY10/ECommerce>
cd ecommerce
```

Create and activate a virtual environment:

```
MacOS:
python -m venv .venv
source .venv/bin/activate

Windows:
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## 5. MySQL Installation
## macOS
Download and install:
https://dev.mysql.com/downloads/mysql/
After installation:
Open System Settings → MySQL
Click Start

## Windows
Download and install:
https://dev.mysql.com/downloads/installer/
Install:
MySQL Server
MySQL Client
MySQL Workbench (optional)
```
mysql -u root -p
```
3. Create the database if not created:
```
CREATE DATABASE ecommerce_db;
```
4. Update authentication plugin:
```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Krishna@10';
FLUSH PRIVILEGES;
```
5. Verify:
```
SELECT user,host,plugin FROM mysql.user;
```

## 6. Django Settings Overview

### Database Configuration
```
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": "ecommerce_db",
    "USER": "root",
    "PASSWORD": "Krishna@10",
    "HOST": "localhost",
    "PORT": "3306",
  }
}
```

### MySQL Connector
```
import pymysql
pymysql.install_as_MySQLdb()
```

### JWT Setup
```
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
}
```

### Stripe Keys
```
STRIPE_PUBLIC_KEY = "<your_public_key>"
STRIPE_SECRET_KEY = "<your_secret_key>"
```

### Static Files
```
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

## 7. Initialize Database

```
python manage.py migrate

```

## 8. Create an Admin User

```
python manage.py createsuperuser

username : admin
email : admin@example.com
password : admin123
```

Start server:
```
python manage.py runserver

```
Access:

sample user
username : krishna
email : krishna@gmail.com
password : mAnjuz-nokheb-4tuxmu

```
http://127.0.0.1:8000/admin/
```

## 9. JWT Authentication Usage

```
POST /api/token/
{ "username": "...", "password": "..." }
```
Refresh:
```
POST /api/token/refresh/
```
Auth Header:
```
Authorization: Bearer <token>
```

## 10. Stripe Usage

- Products handled in `store`
- Orders processed in `checkout`
- Stripe Checkout hosted payment page

## 11. Run Server

```
python manage.py runserver
```

## 12. Troubleshooting

Install cryptography if required:
```
pip install cryptography
```

If auth fails:
```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Krishna@10';
FLUSH PRIVILEGES;
```

Restart MySQL from System Settings.

## 13. Production Notes

- Disable DEBUG
- Move secrets to environment variables
- Restrict ALLOWED_HOSTS
- Use HTTPS

## 14. Status

Configured for local development; production hardening required.
