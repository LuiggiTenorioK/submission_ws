import os
from pathlib import Path
from environs import Env
import json

env = Env()

# Setting DJANGO SECRET KEY
SECRET_KEY = env.str('DJANGO_SECRET_KEY',
                     'd5rgdp(px3o9$lpk^#pr&y1s%5(w#1otyzlrv1#r+q=2@+uf&2')

# The most important thing is to be build relative path
BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration file
CONFIG_PATH = env.str("DRMAATIC_CONFIG_PATH")

if not os.path.isfile(CONFIG_PATH):
    raise RuntimeError("Invalid config file path")

try:
    with open(CONFIG_PATH, "r") as f:
        _config: dict = json.load(f)
except:
    raise RuntimeError("Error reading config file")

# Basic config
DEBUG = _config.get("DEBUG", False)
MAX_PAGE_SIZE = _config.get("MAX_PAGE_SIZE", 1000)

# CLUSTER config
CLUSTER_CONFIG = _config.get("CLUSTER", {})

SUPPORTED_DRM_SYSTEMS = ["SLURM"]
DRM_SYSTEM = CLUSTER_CONFIG.get("DRM_SYSTEM")

if DRM_SYSTEM not in SUPPORTED_DRM_SYSTEMS:
    raise RuntimeError("Unsupported DRM system. Supported systems: {}".format(
        ", ".join(SUPPORTED_DRM_SYSTEMS)))

DRMAA_LIBRARY_PATH = CLUSTER_CONFIG.get("DRMAA_LIBRARY_PATH")
if isinstance(DRMAA_LIBRARY_PATH, str) and os.path.isfile(DRMAA_LIBRARY_PATH):
    # Put as an env variable for the lib
    os.environ.setdefault("DRMAA_LIBRARY_PATH", DRMAA_LIBRARY_PATH)
else:
    raise RuntimeError("Please provide a valid path for DRMAA implementation")

# SUBMISSION APP FOLDERS
SUBMISSION_SCRIPT_DIR = CLUSTER_CONFIG.get(
    'SUBMISSION_SCRIPT_DIR', os.path.join(BASE_DIR, "scripts/"))
SUBMISSION_OUTPUT_DIR = CLUSTER_CONFIG.get(
    'SUBMISSION_OUTPUT_DIR', os.path.join(BASE_DIR, "outputs/"))

SUBMISSION_LOGGER_PTH = CLUSTER_CONFIG.get(
    'SUBMISSION_LOGGER_PTH', os.path.join(BASE_DIR, "logger.log"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "request_formatter": {
            "format": "%(asctime)s - %(name)-20s - %(levelname)-7s - %(ip)-15s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "drm_formatter": {
            "format": "%(asctime)s - %(name)-20s - %(levelname)-7s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "ip_request": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "request_formatter",
            'filters': ['append_ip', 'shorten_name'],
            "filename": SUBMISSION_LOGGER_PTH,
        },
        "drm": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filters": ['shorten_name'],
            "formatter": "drm_formatter",
            "filename": SUBMISSION_LOGGER_PTH,
        },
        "base": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "drm_formatter",
            "filename": SUBMISSION_LOGGER_PTH,
        },
    },
    'filters': {
        'append_ip': {
            '()': 'submission.log.IPAddressFilter'
        },
        'shorten_name': {
            '()': 'submission.log.NameFilter'
        }
    },
    'loggers': {
        'submission_lib': {
            'handlers': ['drm'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'submission': {
            'level': 'INFO',
            'handlers': ['ip_request'],
            'propagate': True,
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['base'],
            'propagate': True,
        },
    },
}

# Set true if you want to remove the task directory when the task is deleted
REMOVE_TASK_FILES_ON_DELETE = CLUSTER_CONFIG.get(
    'REMOVE_TASK_FILES_ON_DELETE', True)


# Security confifg
SECURITY_CONFIG = _config.get("SECURITY", {})

CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOWED_ORIGINS = SECURITY_CONFIG.get("CORS_ALLOWED_ORIGINS", [])
ALLOWED_HOSTS = SECURITY_CONFIG.get("ALLOWED_HOSTS", ['*'])
# HTTPS flags
CSRF_COOKIE_SECURE = SECURITY_CONFIG.get('CSRF_COOKIE_SECURE', False)
SESSION_COOKIE_SECURE = SECURITY_CONFIG.get(
    'SESSION_COOKIE_SECURE', False)
CSRF_TRUSTED_ORIGINS = SECURITY_CONFIG.get('CSRF_TRUSTED_ORIGINS', [])

# OAuth
OAUTH_INTROSPECTION_ENDPOINT = SECURITY_CONFIG.get("OAUTH_INTROSPECTION_ENDPOINT", "")

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DB_CONFIG = _config.get("DATABASE", {})

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_CONFIG.get("NAME"),
        'USER': DB_CONFIG.get("USER"),
        'PASSWORD': DB_CONFIG.get("PASSWORD"),
        'HOST': DB_CONFIG.get("HOST"),
        'PORT': DB_CONFIG.get("PORT"),
    }
}

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
    'submission.renderers.CustomBrowsableAPIRenderer',
)

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'rangefilter',  # Range filter for django admin panel
    'django_filters',  # Django filters for query parameters based filtering
    'django_extensions',
    # 'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'submission.apps.SubmissionConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'submission.pagination.StandardResultsSetPagination',
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
}

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'server.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Define user model
# NOTE https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = 'submission.Admin'

# Define automatic field
# NOTE https://stackoverflow.com/questions/67783120/warning-auto-created-primary-key-used-when-not-defining-a-primary-key-type-by
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
