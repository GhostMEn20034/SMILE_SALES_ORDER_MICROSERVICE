import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", default=0))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

AUTH_USER_MODEL = "accounts.Account"

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Own apps
    'apps.core',
    'apps.accounts',
    'apps.addresses',
    'apps.products',
    'apps.carts',
    'apps.orders',
    'apps.payments',
    'apps.webhooks',
    'apps.recommendations',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'phonenumber_field',
    'django_countries',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'order_microservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'order_microservice.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("SQL_USER", "user"),
        "PASSWORD": os.getenv("SQL_PASSWORD", "password"),
        "HOST": os.getenv("SQL_HOST", "localhost"),
        "PORT": os.getenv("SQL_PORT", "5432"),
        "CONN_MAX_AGE": int(os.getenv("SQL_CONN_MAX_AGE", 0)),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/order_microservice_cache",
    }
}

SESSION_COOKIE_NAME = "orders-sessionid"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    )
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    "SIGNING_KEY": os.getenv("JWT_SIGNING_KEY", SECRET_KEY),
}

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

CORS_ALLOWED_ORIGINS = [
    FRONTEND_BASE_URL,
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AMPQ settings
AMPQ_CONNECTION_URL = os.getenv("AMPQ_CONNECTION_URL")
PRODUCT_CRUD_EXCHANGE_TOPIC_NAME = os.getenv("PRODUCT_CRUD_EXCHANGE_TOPIC_NAME")
USERS_DATA_CRUD_EXCHANGE_TOPIC_NAME = os.getenv("USERS_DATA_CRUD_EXCHANGE_TOPIC_NAME")

# Paypal Settings
PAYPAL_API_BASE_URL = os.getenv("PAYPAL_API_BASE_URL")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
