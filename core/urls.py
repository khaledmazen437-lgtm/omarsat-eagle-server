from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# استيراد ملفات الـ Views
import store.views
import eagle_server.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', store.views.home_view, name='home'),
    path('store/', store.views.store_view, name='store'),
    path('server/', eagle_server.views.server_view, name='server'),
    path('search/', store.views.search_view, name='search'),

    path('channel-files/', store.views.channel_files_center_view, name='channel_files_center'),

    path('about/', store.views.about_us_view, name='about'),
    path('contact/', store.views.contact_us_view, name='contact'),

    path('login/', store.views.login_view, name='login'),
    path('signup/', store.views.signup_view, name='signup'),
    path('logout/', store.views.logout_view, name='logout'),
    path('profile/', store.views.profile_view, name='profile'),

    path('wishlist/', store.views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', store.views.add_to_wishlist, name='add_to_wishlist'),
    path('discounts/', store.views.discounts_view, name='discounts'),

    path('cart/', store.views.cart_view, name='cart'),
    path('checkout/', store.views.checkout, name='checkout'),

    path('product/<int:id>/', store.views.product_details, name='product_details'),

    path('tutorials/', store.views.tutorials_view, name='tutorials'),

    # رابط تفاصيل ملف القنوات (باقي كما هو)
    path('channel-file/<int:id>/', store.views.channel_file_details, name='channel_file_details'),

    path('add-to-cart/<int:product_id>/', store.views.add_to_cart, name='add_to_cart'),
    path('increase-quantity/<int:product_id>/', store.views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:product_id>/', store.views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:product_id>/', store.views.remove_from_cart, name='remove_from_cart'),
    path('add-review/<int:product_id>/', store.views.add_review, name='add_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
