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
    'jazzmin',
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


# ==========================================
# 🎨 إعدادات شكل لوحة التحكم (Jazzmin)
# ==========================================

JAZZMIN_SETTINGS = {
    # العناوين
    "site_title": "Omar Sat Admin",
    "site_header": "Omar Sat",
    "site_brand": "Omar Sat System",
    "welcome_sign": "مرحباً بك في لوحة تحكم عمر سات 🚀",
    "copyright": "Omar Sat Ltd",
    
    # الأيقونات للقائمة الجانبية
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.Product": "fas fa-box-open",
        "store.Order": "fas fa-shopping-cart",
        "store.Review": "fas fa-star",
        "eagle_server.ServerPlan": "fas fa-server",
        "eagle_server.ServerReport": "fas fa-chart-line",
        "eagle_server.ServerNews": "fas fa-newspaper",
    },
    
    # خيارات العرض
    "show_ui_builder": False, # اقفلها لما تستقر على الشكل
    "changeform_format": "horizontal_tabs",
}

# 🌑 الثيم الغامق (Dark Theme) 🌑
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "theme": "cyborg",  # 👈 ده الثيم الغامق اللي بيليق مع النيون
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# في ملف settings.py

# 1. للسماح بالتضمين الآمن:
X_FRAME_OPTIONS = 'SAMEORIGIN'

# 2. لتشغيل iframes بشكل عام، نحتاج لتعريف نطاقات آمنة (إذا كنت تستخدم مكتبة خارجية)
# إذا كنت تستخدم Django الأساسي، هذا الكود غير مطلوب عادة، لكن يضمن الأمان:
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"