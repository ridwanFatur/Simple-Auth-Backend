# Django Simple Authentication System

A Django project implementing JWT authentication with email verification and two-factor authentication (2FA).

## Features

- JWT Token-based authentication
- Email verification for new accounts
- Two-factor authentication (2FA)
- Google OAuth integration
- Customizable admin URL path
- Comprehensive logging system

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ridwanFatur/django-simple-auth.git
   cd django-simple-auth
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (see Environment Variables section below)

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file in the project root and set the following environment variables:

### Security
```
FRONTEND_URL=http://localhost:3000  # URL of your frontend app
SITE_URL=http://localhost:8000      # URL of this Django app
SECRET_KEY=your_secret_key          # Django secret key
ALLOWED_HOSTS=localhost,127.0.0.1   # Comma-separated list of allowed hosts
DEBUG=True                          # Set to False in production
ADMIN_PATH_URL=admin                # Custom admin URL path
```

### Database
```
PGDATABASE=django_auth_db           # PostgreSQL database name
PGUSER=postgres                     # PostgreSQL username
PGHOST=localhost                    # PostgreSQL host
PGPASSWORD=your_password            # PostgreSQL password
PGPORT=5432                         # PostgreSQL port
```

### Google OAuth Settings
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Email Configuration
```
EMAIL_HOST=smtp.gmail.com           # SMTP server host
EMAIL_PORT=587                      # SMTP server port
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### Logging
```
LOG_HANDLER=console                 # Options: console, file
LOG_FORMATTER=verbose               # Options: simple, verbose
LOG_LEVEL=INFO                      # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```
