from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator 

# ==========================================
# 1. جدول المنتجات (Product) - التعريف الوحيد والكامل
# ==========================================
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('receiver', 'رسيفرات (Receivers)'),
        ('lnb', 'عدسات وأطباق (LNB & Dishes)'),
        ('cable', 'كابلات ووصلات (Cables)'),
        ('remote', 'ريموتات (Remotes)'),
        ('tools', 'أدوات تركيب (Installation Tools)'),
        ('accessories', 'إكسسوارات (Accessories)'),
        ('maintenance', 'قطع غيار صيانة (Spare Parts)'),
    ]

    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    description = models.TextField(verbose_name="وصف المنتج", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة المنتج")
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='receiver', verbose_name="القسم")
    shipping_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="رسوم الشحن لهذا المنتج")
    wifi_support = models.BooleanField(default=False, verbose_name="يدعم الواي فاي؟")
    
    processor = models.CharField(max_length=100, blank=True, null=True, verbose_name="المعالج (Processor)")
    ram = models.CharField(max_length=50, blank=True, null=True, verbose_name="الرامات (RAM)")
    storage = models.CharField(max_length=50, blank=True, null=True, verbose_name="ذاكرة التخزين (Storage)")
    resolution = models.CharField(max_length=50, blank=True, null=True, verbose_name="الجودة (Resolution)")
    tuner_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="نوع التيونر (Tuner)")


    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

# ==========================================
# 2. جدول التقييمات (Review)
# ==========================================
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="المنتج")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="العميل")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم (من 5)"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="التعليق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التقييم")
    
    def __str__(self):
        return f"تقييم {self.rating} نجوم من {self.user.username} على {self.product.name}"
    
    class Meta:
        ordering = ['-created_at'] 
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"

# ==========================================
# 3. جداول السلة (Cart & CartItem)
# ==========================================
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)

# ==========================================
# 4. جداول الطلبات (Order & OrderItem)
# ==========================================
class Order(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'دفع عند الاستلام (Cash) 🚚'),
        ('vodafone', 'فودافون كاش (Vodafone Cash) 📱'),
        ('instapay', 'إنستا باي (InstaPay) 🏦'),
        ('visa', 'فيزا / ماستر كارد (Visa/Mastercard) 💳'),
        ('paypal', 'باي بال (PayPal) 🅿️'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة ⏳'),
        ('processing', 'جاري التجهيز ⚙️'),
        ('shipped', 'تم الشحن 🚚'),
        ('delivered', 'تم التسليم ✅'),
        ('cancelled', 'ملغي ❌'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="العميل", null=True, blank=True)
    
    # 🚨🚨 الحل النهائي لخطأ NOT NULL (السماح بـ NULL في الداتابيز) 🚨🚨
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="الاسم بالكامل")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, null=True, verbose_name="العنوان بالتفصيل")
    
    city = models.CharField(max_length=50, blank=True, default="", null=True, verbose_name="المدينة/المحافظة")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_screenshot = models.ImageField(upload_to='payment_receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True, verbose_name="Client IP") # تم التأكد من null=True

    def __str__(self):
        return f"طلب رقم #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"