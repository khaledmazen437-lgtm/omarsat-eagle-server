from django.contrib import admin
from django.utils.html import format_html
# ✅ تم استيراد TutorialVideo هنا
from .models import Product, Order, OrderItem, Cart, CartItem, Review, ChannelFile, Wishlist, HomeBanner, TutorialVideo 

# 1. تخصيص لوحة المنتجات (Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # ✅ إضافة حقل السعر بعد الخصم (discount_price) في قائمة العرض
    list_display = ['name', 'price', 'discount_price', 'category', 'wifi_support']
    list_filter = ['category', 'wifi_support']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('بيانات أساسية', {
            # ✅ إضافة حقل السعر بعد الخصم (discount_price) في شاشة التعديل
            'fields': ('name', 'description', 'price', 'discount_price', 'image', 'category', 'shipping_fee')
        }),
        ('مواصفات فنية (اختياري)', {
            'fields': ('processor', 'ram', 'storage', 'resolution', 'tuner_type', 'wifi_support'),
            'classes': ('collapse',), 
        }),
    )


# 2. تخصيص لوحة الطلبات (Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_price', 'quantity'] 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone_number', 'total_price', 'status', 'payment_status_thumbnail', 'created_at']
    list_filter = ['status', 'created_at', 'payment_method']
    search_fields = ['full_name', 'phone_number', 'id']
    inlines = [OrderItemInline]
    
    readonly_fields = ['created_at', 'view_payment_screenshot', 'total_price']

    def view_payment_screenshot(self, obj):
        if obj.payment_screenshot:
            return format_html('<img src="{}" style="max-height:150px; border-radius:5px;" />', obj.payment_screenshot.url)
        return "لم يتم إرفاق صورة تحويل"
    view_payment_screenshot.short_description = "صورة إثبات الدفع"

    def payment_status_thumbnail(self, obj):
        if obj.payment_screenshot:
            return format_html('<img src="{}" style="max-height:30px; border-radius:5px;" title="صورة تحويل مرفقة" />', obj.payment_screenshot.url)
        return "❌"
    payment_status_thumbnail.short_description = "صورة دفع"
    
    fieldsets = (
        ('بيانات العميل', {'fields': ('user', 'full_name', 'phone_number', 'address', 'city')}),
        ('تفاصيل الدفع والحالة', {'fields': ('total_price', 'payment_method', 'status', 'view_payment_screenshot')}),
    )

# 3. تخصيص لوحة ملفات القنوات
@admin.register(ChannelFile)
class ChannelFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'device_type', 'date_added', 'view_link_button'] 
    list_filter = ['device_type', 'date_added']
    search_fields = ['title', 'compatible_devices']
    ordering = ['-date_added']
    
    fieldsets = (
        ('البيانات الأساسية', {'fields': ('title', 'device_type', 'image', 'download_link')}),
        ('التفاصيل والمواصفات', {'fields': ('description', 'compatible_devices')}),
    )

    def view_link_button(self, obj):
        return format_html('<a class="button" href="{}" target="_blank">🔗 فتح الرابط</a>', obj.download_link)
    view_link_button.short_description = "معاينة الرابط"

# 4. تخصيص لوحة المفضلة
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date_added')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('user', 'product', 'date_added')

# 5. تخصيص وتسجيل لوحة البانرات الجديدة (HomeBanner)
@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'ordering', 'image_preview')
    list_editable = ('is_active', 'ordering')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    
    # دالة لعرض صورة مصغرة للبانر في قائمة الإدارة
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.image.url)
        return "لا توجد صورة"
    image_preview.short_description = "معاينة"

# ✅ 6. تخصيص وتسجيل لوحة الشروحات والفيديوهات الجديدة (TutorialVideo)
@admin.register(TutorialVideo)
class TutorialVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'is_active')
    list_filter = ('is_active', 'date_added')
    search_fields = ('title', 'description')
    date_hierarchy = 'date_added'
    
    fieldsets = (
        ('بيانات الفيديو', {'fields': ('title', 'description', 'video_url', 'is_active')}),
    )


# تسجيل النماذج البسيطة (لم تتغير)
if not admin.site.is_registered(Review):
    admin.site.register(Review)
if not admin.site.is_registered(Cart):
    admin.site.register(Cart)
if not admin.site.is_registered(CartItem):
    admin.site.register(CartItem)