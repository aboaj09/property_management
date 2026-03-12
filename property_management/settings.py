"""
Django settings for property_management project.
"""

import os
import dj_database_url
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import sys

print("DATABASE_URL =", os.getenv('DATABASE_URL'))

BASE_DIR = Path(__file__).resolve().parent.parent

# متغيرات البيئة
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# النطاقات المسموح بها (أضف نطاق Vercel الخاص بك بعد النشر)
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.now.sh']

# CSRF
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://*.vercel.app,https://*.now.sh').split(',')

# WSGI
WSGI_APPLICATION = 'property_management.wsgi.app'

# التطبيقات
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Cloudinary للتخزين
    'cloudinary_storage',
    'cloudinary',
    # التطبيق الخاص
    'rentals',
]

# Middleware
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

# قاعدة البيانات
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

# التحقق من كلمة المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والوقت
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

# الملفات الثابتة (Static files)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================
# إعدادات Cloudinary (للملفات المرفوعة)
# ============================================================
# يجب تعيين هذه المتغيرات في بيئة التشغيل (Environment Variables)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('dzsipctqe'),
    'API_KEY': os.getenv('484654375992933'),
    'API_SECRET': os.getenv('0yNVYUP89D-YzYtX1kzgljM7N9E'),
}

# استخدام Cloudinary كمخزن افتراضي للملفات (Media files)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# يمكن إزالة أو تعليق MEDIA_URL و MEDIA_ROOT لأن Cloudinary سيتولى الأمر
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

# Content Security Policy (CSP)
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