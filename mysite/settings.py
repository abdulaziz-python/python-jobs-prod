import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = os.environ.get('BASE_URL', 'https://localhost:8000')

if not BASE_URL:
    raise ImproperlyConfigured("BASE_URL is not set in the environment variables")

SECRET_KEY = 'your-secret-key'

DEBUG = False


ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projects',
    "vercel",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pyjobs',
        'USER': 'pyjobs_user',
        'PASSWORD': 'yxFDAWFP5i1kbr8XDl3hBwVoPSQ0VRMR',
        'HOST': 'dpg-cv26bthu0jms738qlql0-a.oregon-postgres.render.com',
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




LANGUAGE_CODE = 'uz'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('uz', 'O\'zbek'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, '/static')]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ablaze.crypto.king@gmail.com' 
EMAIL_HOST_PASSWORD = 'tbwf gcqh vncc ygqi'  
DEFAULT_FROM_EMAIL = 'ablaze.crypto.king@gmail.com'

AUTH_USER_MODEL = 'projects.CustomUser'



CSRF_TRUSTED_ORIGINS = [
    'https://1e8e-213-230-92-56.ngrok-free.app',
    'https://localhost:8000',
    'https://pyjobs.onrender.com',
    'https://8000-idx-course-1736610940535.cluster-blu4edcrfnajktuztkjzgyxzek.cloudworkstations.dev',
    'https://9000-idx-course-1736610940535.cluster-blu4edcrfnajktuztkjzgyxzek.cloudworkstations.dev',
]







