import os

DEBUG = os.environ.get("DEBUG").lower() in ("true", "1", "t")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(",")

SECRET_KEY = os.environ.get("SECRET_KEY")
SITE_URL = os.getenv("SITE_URL")

FRONTEND_URL = os.environ.get("FRONTEND_URL")
CORS_ALLOWED_ORIGINS = os.environ.get("FRONTEND_URL").split(",")
ADMIN_URL = os.environ.get("ADMIN_PATH_URL")
