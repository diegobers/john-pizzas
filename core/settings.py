import environ
import os
import dj_database_url
from pathlib import Path

from django.utils.translation import gettext_lazy as _


env = environ.Env()

# Set the project base directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env.bool("DEBUG", default=True)

SECRET_KEY = env("RAILWAY_SECRET")

AUTH_USER_MODEL = 'accounts.JohnPizzaAbstractUserModel'

SESSION_COOKIE_NAME = 'store'

#SESSION_SAVE_EVERY_REQUEST = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

ALLOWED_HOSTS = env.list('HOSTS')

SITE_ID = 1

INTERNAL_IPS = [
    '127.0.0.1',
]

CSRF_ALLOWED_ORIGINS = ['https://john-pizzas-production.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://john-pizzas-production.up.railway.app']
CORS_ORIGINS_WHITELIST = ['https://john-pizzas-production.up.railway.app']

# App's
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # my app's
    'accounts',
    #'orders',
    'pages',
    #'cart',
    'django_bootstrap5',
    'store',
    # third lib
    'debug_toolbar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'widget_tweaks',

]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR , 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'store.context_processors.cart_items_count',
            ],



        },
    },
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = { 
    'default': dj_database_url.config(default=os.environ["DATABASE_URL"]),
}
#DATABASES = {
#    "default": env.db("SQLITE_URL"), DATABASE_URL RAILWAY_URL
#}

# Password validation
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
LANGUAGE_CODE = 'pt-Br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ('pt-br', _('Brasil')),
]

# Static files
STATICFILES_DIRS = [ os.path.join(BASE_DIR , "static") ]
STATIC_ROOT = os.path.join(BASE_DIR , "staticfiles")
STATIC_URL = env.str("STATIC_URL", default="static/")


# Base url to serve media files
MEDIA_URL = '/media/'
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Auth
ACCOUNT_FORMS = {'login': 'accounts.forms.CustomAllAuthLoginForm'}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST') 
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Redefinir Senha!'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'store:index'
LOGOUT_REDIRECT_URL = 'store:index'

#ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = LOGIN_REDIRECT_URL
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CHANGE_EMAIL = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
#ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = settings.LOGIN_URL
#ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None -> settings.LOGIN_REDIRECT_URL
#ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
#ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_NOTIFICATIONS = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'http://john-pizzas-production.com'
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
#ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGOUT_ON_GET = True
#ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
#ACCOUNT_LOGOUT_REDIRECT_URL = settings.LOGOUT_REDIRECT_URL
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_PRESERVE_USERNAME_CASING = True
#ACCOUNT_PREVENT_ENUMERATION = True
ACCOUNT_REAUTHENTICATION_TIMEOUT = 300
ACCOUNT_REAUTHENTICATION_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
#ACCOUNT_SIGNUP_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
ACCOUNT_TEMPLATE_EXTENSION = 'html'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_USERNAME_REQUIRED = False

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}