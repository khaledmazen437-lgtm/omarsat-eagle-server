from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# 🛑 الحـل: استيراد ملفات الـ Views كوحدات (Modules) 🛑
import store.views 
import eagle_server.views 

# 2. الروابط الرئيسية
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # الصفحات الأساسية
    path('', store.views.home_view, name='home'),
    path('store/', store.views.store_view, name='store'),
    path('server/', eagle_server.views.server_view, name='server'), 
    path('search/', store.views.search_view, name='search'),

    # صفحات المعلومات (نستخدم الدالة التي ترجع لـ 'home' في views.py)
    path('about/', store.views.about_us_view, name='about'),
    path('contact/', store.views.contact_us_view, name='contact'),

    # الحسابات
    path('login/', store.views.login_view, name='login'),
    path('signup/', store.views.signup_view, name='signup'),
    path('logout/', store.views.logout_view, name='logout'),
    path('profile/', store.views.profile_view, name='profile'),
    
    # السلة والدفع والمنتجات
    path('cart/', store.views.cart_view, name='cart'),
    path('checkout/', store.views.checkout, name='checkout'),
    
    # تفاصيل المنتج
    path('product/<int:id>/', store.views.product_details, name='product_details'),
    
    # 🚨🚨 عمليات التحكم في السلة (الزيادة والنقصان والحذف) 🚨🚨
    path('add-to-cart/<int:product_id>/', store.views.add_to_cart, name='add_to_cart'),
    
    # 👇 تم إضافة الروابط المفقودة لتمكين التحكم في الكمية 👇
    path('increase-quantity/<int:product_id>/', store.views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:product_id>/', store.views.decrease_quantity, name='decrease_quantity'),
    
    path('remove-from-cart/<int:product_id>/', store.views.remove_from_cart, name='remove_from_cart'),
    path('add-review/<int:product_id>/', store.views.add_review, name='add_review'),
]

# 3. كود تحميل الصور (Media & Static)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)