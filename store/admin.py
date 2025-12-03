from django.contrib import admin
from django.utils.html import format_html
# تأكد أنك تستورد كل النماذج التي ستسجلها
from .models import Product, Order, OrderItem, Cart, CartItem, Review

# 1. تخصيص لوحة المنتجات (Product)
@admin.register(Product) # 👈 استخدام Decorator
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'wifi_support']
    list_filter = ['category', 'wifi_support']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('بيانات أساسية', {
            'fields': ('name', 'description', 'price', 'image', 'category', 'shipping_fee')
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

@admin.register(Order) # 👈 استخدام Decorator
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

# 3. تسجيل النماذج البسيطة (باستخدام الطريقة الآمنة)
# نستخدم is_registered لأنها موديلات بسيطة لا تحتاج AdminClass مخصص
if not admin.site.is_registered(Review):
    admin.site.register(Review)
if not admin.site.is_registered(Cart):
    admin.site.register(Cart)
if not admin.site.is_registered(CartItem):
    admin.site.register(CartItem)