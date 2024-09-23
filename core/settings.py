"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


# import logging
# import os
#
# # Визначте шлях до каталогу логів
# log_dir = os.path.join(BASE_DIR, 'core', 'log')
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)
#
# # Налаштування об'єктів логування
# file_log = logging.FileHandler(os.path.join(log_dir, "api_backend.log"))
# console_out = logging.StreamHandler()
#
# # Налаштування форматування логування
# logging.basicConfig(
#     handlers=(file_log, console_out),
#     level=logging.INFO,
#     datefmt="%d.%m.%Y %H:%M:%S",
#     format="[%(asctime)s loglevel=%(levelname)-6s]:  %(message)s ||| \
# call_trace=%(pathname)s L%(lineno)-4d ",
# )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    # "http://localhost:80",
    # "http://localhost:8000",
    # "http://localhost:7777",
    # "https://localhost:3001",
    # "http://localhost:3000",
    # "http://localhost:3339",
    # "https://localhost:3339",
    # "http://localhost:5001",
    # "https://localhost:5001",
    # "https://api-backend.naratyv-creative.fun",
    # "http://213.199.63.47:7777",
    # "http://213.199.63.47:3339",
    # "https://213.199.63.47:3339",
    # "http://213.199.63.47:5001",
    # "https://213.199.63.47:5001",
    "*",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "drf_yasg",
    "debug_toolbar",
    "taggit",
    "corsheaders",
    # user app
    "players.apps.PlayersConfig",
    "developers.apps.DevelopersConfig",
    "catalog.apps.CatalogConfig",
    "gallery.apps.GalleryConfig",
    "game_session.apps.GameSessionConfig",
    "api.v1.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 3rd party
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # user middleware
    # 'accounts.middleware.ValidationErrorMiddleware',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres_pass"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres_service"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.\
            UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

USE_I18N = False
USE_L10N = False
USE_TZ = True

DATE_FORMAT = "d-m-Y"
DATETIME_FORMAT = "d b Y - H:i:s"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "nginx", "vol", "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TODO Change after creating User model
# AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = 1

INTERNAL_IPS = ["127.0.0.1"]

# TODO Change lifetime if it will be needed
ACCESS_TOKEN_LIFETIME = timedelta(days=1)
REFRESH_TOKEN_LIFETIME = timedelta(days=5)


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "EXCEPTION_HANDLER": "api.v1.exceptions.custom_exception_handler",
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
]

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:80",
#     "http://localhost:8000",
#     "http://localhost:7777",
#     "https://localhost:3001",
#     "http://localhost:3000",
#     "http://localhost:3339",
#     "https://localhost:3339",
#     "http://localhost:5001",
#     "https://localhost:5001",
#     "https://api-backend.naratyv-creative.fun",
#     "http://213.199.63.47:7777",
#     "http://213.199.63.47:3339",
#     "https://213.199.63.47:3339",
#     "http://213.199.63.47:5001",
#     "https://213.199.63.47:5001",
# ]

SWAGGER_SETTINGS = {
    "FORM_METHOD": "POST",
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Token Auth": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

REDIS_HOST = os.getenv("REDIS_HOST", "redis_container_service")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

DEFAULT_CHARSET = "utf-8"
#
# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:80",
#     "http://localhost:8000",
#     "http://localhost:7777",
#     "https://localhost:3001",
#     "http://localhost:3000",
#     "http://localhost:3339",
#     "https://localhost:3339",
#     "http://localhost:5001",
#     "https://localhost:5001",
#     "https://api-backend.naratyv-creative.fun",
#     "http://213.199.63.47:7777",
#     "http://213.199.63.47:3339",
#     "https://213.199.63.47:3339",
#     "http://213.199.63.47:5001",
#     "https://213.199.63.47:5001",
# ]


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
