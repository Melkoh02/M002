import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--011y2@^^x!+)jeybm^@)4@vpia7m$^7c9(t-+$10d%_c+4*%8'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '*'
]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'users.apps.UsersConfig',
    'rest_framework',
    'drf_spectacular',
    'dj_rest_auth',
    'rest_framework.authtoken',
    'corsheaders',
    'cities_light',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

JAZZMIN_SETTINGS = {
    "site_title": "M002",
    "site_header": "M002",
    "site_brand": "M002",
    "welcome_sign": "Welcome to the Admin Panel",
    # "copyright": "M002",
    "search_model": "auth.User",
    "user_avatar": None,
    # Custom icons for models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.User": "fas fa-users",
    },
    # Customization of top menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "auth"},
    ],
    # Custom links to be included in the user menu
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],
    # Whether to show or hide the side menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "auth.user", "auth.Group"],
    # "custom_links": {
    #     "auth": [{
    #         "name": "Make Messages", "url": "make_messages", "icon": "fas fa-comments",
    #         "permissions": ["auth.view_user"]
    #     }]
    # },
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

WSGI_APPLICATION = 'djangoProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}

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
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'M002 API',
    'DESCRIPTION': 'M002 Endpoints',
    'VERSION': '1.0.0',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

CORS_ALLOW_ALL = DEBUG
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
    'http://0.0.0.0:3000',
    'https://serviciosymandatos.com.py',
    'https://www.serviciosymandatos.com.py',
    'https://www.aguapuraamerica.com',
    'https://aguapuraamerica.com'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://0.0.0.0:3000',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
    'https://serviciosymandatos.com.py',
    'https://www.serviciosymandatos.com.py',
    'https://aguapuraamerica.com'
    'https://www.aguapuraamerica.com'
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"

CITIES_LIGHT_DATA_DIR = os.path.join(BASE_DIR, 'cities')
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['es']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['PY']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
