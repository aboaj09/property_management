"""
Django settings for property_management project.
"""

import os
import dj_database_url
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ... باقي الإعدادات ...

# السماح لنطاقات Vercel
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.now.sh']

# 🔴 تأكد من هذا السطر (يجب أن يشير إلى `app` في wsgi.py)
WSGI_APPLICATION = 'property_management.wsgi.app'

# إعدادات الملفات الثابتة (static)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ملفات الوسائط (ملفات المستخدمين) - Vercel لا يدعمها محلياً!
# إذا كنت تستخدم رفع الصور، ستحتاج Cloudinary أو خدمة تخزين خارجية
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# تأكد من أن DEBUG=False
DEBUG = False

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://amar.up.railway.app,https://*.up.railway.app').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rentals',  # تطبيق إدارة الإيجارات
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'property_management.urls'

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

WSGI_APPLICATION = 'property_management.wsgi.application'

# Database
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ar'
LANGUAGES = [
    ('ar', _('العربية')),
    ('en', _('English')),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (Uploaded files) - استخدام التخزين المحلي مؤقتاً
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# إعدادات تسجيل الدخول والجلسة
# ============================================================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
SESSION_COOKIE_AGE = 1800  # 30 دقيقة
SESSION_SAVE_EVERY_REQUEST = True

# ============================================================
# إعدادات الأمان (للإنتاج)
# ============================================================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Content Security Policy (معدلة للسماح بالأيقونات)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", 
                  "cdn.jsdelivr.net", "fonts.googleapis.com", 
                  "cdnjs.cloudflare.com", "code.jquery.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", 
                 "cdn.jsdelivr.net", "fonts.googleapis.com", 
                 "cdnjs.cloudflare.com")
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com", "cdn.jsdelivr.net", 
                "cdnjs.cloudflare.com", "data:")
CSP_IMG_SRC = ("'self'", "data:", "cdn.jsdelivr.net")
CSP_CONNECT_SRC = ("'self'",)
CSP_MEDIA_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_INCLUDE_NONCE_IN = ('script-src',)