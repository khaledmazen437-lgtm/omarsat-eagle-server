from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator 

# ==========================================
# 1. جدول المنتجات (Product) - التعريف الوحيد والكامل
# ==========================================
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('receivers', 'ريسيفرات'),
        ('lnb', 'عدسات LNB'),
        ('remotes', 'ريموتات'),
        ('dish_acc', 'اكسسوارات دش'),
        ('mobile_acc', 'اكسسوارات موبايل'),
        ('pc_acc', 'اكسسوارات كمبيوتر ولاب توب'),
        ('cctv', 'كاميرات مراقبة'),
        ('other_acc', 'اكسسوارات اخري'),
    ]

    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    description = models.TextField(verbose_name="وصف المنتج", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة المنتج")
    
    # ✅ الإضافة الجديدة: حقل السعر بعد الخصم
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="السعر بعد الخصم"
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='receivers', verbose_name="القسم")
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
        # يستخدم السعر المخفض إذا كان موجوداً، وإلا يستخدم السعر الأصلي
        price_to_use = self.product.discount_price if self.product.discount_price else self.product.price
        return price_to_use * self.quantity

    def __str__(self):
        return str(self.product)

# ==========================================
# 4. جداول الطلبات (Order & OrderItem)
# ==========================================
class Order(models.Model):
    # ✅ قائمة الدفع المحدثة (فودافون كاش وإنستا باي فقط)
    PAYMENT_METHODS = [
        ('vodafone', 'فودافون كاش 📱'),
        ('instapay', 'إنستا باي 🏦'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة ⏳'),
        ('processing', 'جاري التجهيز ⚙️'),
        ('shipped', 'تم الشحن 🚚'),
        ('delivered', 'تم التسليم ✅'),
        ('cancelled', 'ملغي ❌'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="العميل", null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="الاسم بالكامل")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, null=True, verbose_name="العنوان بالتفصيل")
    
    city = models.CharField(max_length=50, blank=True, default="", null=True, verbose_name="المدينة/المحافظة")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # ⚠️ Default value must be updated since 'cod' is removed (setting to vodafone cash)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='vodafone') 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_screenshot = models.ImageField(upload_to='payment_receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True, verbose_name="Client IP")

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
    
# ==========================================
# 5. جدول ملفات القنوات (ChannelFile)
# ==========================================

class ChannelFile(models.Model):
    DEVICE_CHOICES = [
        ('sunplus', 'Sunplus (صن بلص)'),
        ('gx', 'GX (جي إكس)'),
        ('android', 'Android / TV Box'),
        ('other', 'أخرى'),
    ]

    title = models.CharField(max_length=200, verbose_name="اسم الملف")
    device_type = models.CharField(max_length=50, choices=DEVICE_CHOICES, verbose_name="نوع الجهاز")
    image = models.ImageField(upload_to='channel_files/', blank=True, null=True, verbose_name="صورة الرسيفر")
    
    description = models.TextField(verbose_name="تفاصل ومواصفات الملف", blank=True, null=True)
    compatible_devices = models.TextField(verbose_name="أسماء الرسيفرات المدعومة (اكتب كل رسيفر في سطر)", blank=True, null=True)
    
    download_link = models.URLField(verbose_name="رابط التحميل")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ملف قنوات"
        verbose_name_plural = "📂 مركز ملفات القنوات"

# ==========================================
# 6. جدول المفضلة (Wishlist)
# ==========================================

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "مفضلة"
        verbose_name_plural = "قائمة المفضلة"
        # ضمان أن المستخدم لا يضيف نفس المنتج مرتين
        unique_together = ('user', 'product') 

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.name}"
    
# ==========================================
# 7. جدول البانرات (HomeBanner)
# ==========================================

class HomeBanner(models.Model):
    title = models.CharField(max_length=150, verbose_name="العنوان الرئيسي")
    subtitle = models.CharField(max_length=250, verbose_name="الوصف الفرعي", blank=True, null=True)
    image = models.ImageField(upload_to='banners/', verbose_name="صورة العرض")
    link = models.URLField(max_length=200, verbose_name="رابط المنتج/الخصم (اختياري)", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="نشط/مُفعّل")
    ordering = models.IntegerField(default=0, verbose_name="ترتيب الظهور")

    class Meta:
        verbose_name = "بانر رئيسي (شريط العروض)"
        verbose_name_plural = "بانرات العروض الرئيسية"
        ordering = ['ordering', '-id']

    def __str__(self):
        return self.title

# ===============================================
# ✅ 8. موديل الشروحات والفيديوهات الجديد (TutorialVideo)
# ===============================================

class TutorialVideo(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الشرح/الفيديو")
    description = models.TextField(verbose_name="الوصف المختصر", null=True, blank=True)
    video_url = models.URLField(verbose_name="رابط الفيديو (YouTube/Embed)", help_text="ضع رابط الفيديو مباشرة (يفضل رابط تضمين Embed)")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    is_active = models.BooleanField(default=True, verbose_name="نشط/ظاهر")

    class Meta:
        verbose_name = "فيديو شرح/تطبيق"
        verbose_name_plural = "📺 الشروحات والفيديوهات"
        ordering = ['-date_added']

    def __str__(self):
        return self.title
# في ملف store/models.py، داخل كلاس TutorialVideo

    # دالة مساعدة لاستخراج رابط التضمين (Embed URL)
    def get_embed_url(self):
        # 1. إذا كان الرابط هو رابط مشاهدة عادي (watch?v=)
        if 'youtube.com/watch?v=' in self.video_url:
            # نستخرج الـ ID ونحول الرابط إلى صيغة Embed
            video_id = self.video_url.split('v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
            
        # 2. إذا كان الرابط هو رابط قصير (youtu.be/)
        elif 'youtu.be/' in self.video_url:
            # نستخرج الـ ID ونحول الرابط إلى صيغة Embed
            video_id = self.video_url.split('/')[-1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
            
        # 3. إذا لم يكن رابط يوتيوب، نرجعه كما هو (قد يكون رابط Embed مباشر)
        return self.video_url