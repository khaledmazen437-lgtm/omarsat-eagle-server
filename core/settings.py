import os
from pathlib import Path
from django.contrib.messages import constants as messages

# 1. تحديد مسار المشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. مفتاح الأمان (يفضل تغييره عند الرفع الحقيقي)
SECRET_KEY = 'django-insecure-example-key-change-this-in-production' 

# 🚨🚨 هام: اجعلها True أثناء التجربة، و False عند الرفع النهائي
DEBUG = True 

# 3. المضيفون المسموح لهم
# النجمة * تسمح بالعمل على Ngrok و PythonAnywhere و Localhost دون مشاكل
ALLOWED_HOSTS = ['*'] 


# 4. التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # تطبيقاتنا
    'store',
    'eagle_server',
]

# 5. البرمجيات الوسيطة (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# 6. القوالب (Templates)
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
                # مهم جداً للصور
                'django.template.context_processors.media', 
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# 7. قاعدة البيانات (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 8. التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# 9. اللغة والوقت
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Cairo' 
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==========================================
# 10. ملفات Static (CSS, JS, Images)
# ==========================================
STATIC_URL = '/static/'

# المكان اللي انت بتخزن فيه ملفاتك وانت شغال
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'store', 'static'),
]

# 🚨🚨 هذا السطر مهم جداً عند الرفع (مكان تجميع الملفات) 🚨🚨
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==========================================
# 11. ملفات Media (صور المنتجات والتحويلات)
# ==========================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================
# 12. إعدادات الدخول والروابط
# ==========================================
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# 13. إعدادات الأمان (HTTPS & CSRF)
# ==========================================

# السماح للروابط الخارجية (Ngrok + Localhost + Hosting)
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000', 
    'http://localhost:8000',
    'https://*.ngrok-free.dev',      # للسماح لـ Ngrok
    'https://*.ngrok-free.app',      # دومين Ngrok الآخر
    'https://*.pythonanywhere.com'   # لو هترفع على PythonAnywhere
]

# ⚠️ إعدادات الكوكيز (اجعلها False طالما ليس لديك HTTPS حقيقي ودومين خاص)
CSRF_COOKIE_SECURE = False 
SESSION_COOKIE_SECURE = False 

# تخصيص عنوان لوحة التحكم
ADMIN_SITE_HEADER = 'لوحة تحكم Omar Sat'