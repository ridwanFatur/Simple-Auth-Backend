# flake8: noqa

import os
from pathlib import Path

from dotenv import load_dotenv

## Setup
BASE_DIR = Path(__file__).resolve().parent.parent
DOT_ENV = os.environ.get("DOT_ENV", os.path.join(BASE_DIR, ".env"))
load_dotenv(dotenv_path=DOT_ENV, override=True)

## Default
# Application definition
INSTALLED_APPS = [
    # Default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    # Local apps
    "core",
    "users",
    "user_settings",
]

# Middleware
MIDDLEWARE = [
		# Extended
    "corsheaders.middleware.CorsMiddleware",
    # Default
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

## Extended settings
from core.extended_settings.database import *
from core.extended_settings.default import *
from core.extended_settings.email_settings import *
from core.extended_settings.google_settings import *
from core.extended_settings.jwt_settings import *
from core.extended_settings.logging import *
from core.extended_settings.security import *
