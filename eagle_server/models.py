from django.db import models

# ==========================================
# 1. موديل الباقات (للمبيعات)
# ==========================================
class ServerPlan(models.Model):
    SERVER_TYPES = [
        ('iptv', 'IPTV (قنوات وأفلام)'),
        ('cccam', 'CCcam / Sharing (شيرنج أقمار)'),
        ('working', 'الباقات العاملة'), 
    ]

    name = models.CharField(max_length=100, verbose_name="اسم الباقة")
    server_type = models.CharField(max_length=20, choices=SERVER_TYPES, default='iptv', verbose_name="نوع الخدمة")
    duration = models.IntegerField(verbose_name="المدة (شهور)", default=12)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="السعر")
    features = models.TextField(verbose_name="المميزات", blank=True, null=True)
    
    # 🚨🚨 إضافة حقل الصورة للباقات (لتظهر في الواجهة) 🚨🚨
    image = models.ImageField(upload_to='plan_images/', verbose_name="صورة الباقة", blank=True, null=True)


    def __str__(self):
        return f"{self.name} ({self.get_server_type_display()})"

    class Meta:
        verbose_name = "باقة سيرفر"
        verbose_name_plural = "باقات إيجل سات"


# ==========================================
# 2. موديل الأخبار والتحديثات
# ==========================================
class ServerNews(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الخبر")
    content = models.TextField(verbose_name="تفاصيل الخبر", blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_posted']
        verbose_name = "خبر"
        verbose_name_plural = "أخبار وتحديثات السيرفر"

# ==========================================
# 3. موديل تقارير الباقات العاملة (القسم الرئيسي الجديد)
# ==========================================
class ServerReport(models.Model):
    STATUS_CHOICES = [
        ('Active', '🟢 نشط'),
        ('Maintenance', '🟡 صيانة'),
        ('Down', '🔴 متوقف'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="اسم الباقة/الخادم")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', verbose_name="حالة التشغيل")
    report_details = models.TextField(verbose_name="تفاصيل/ملاحظات التقرير", blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")
    
    # 🚨🚨 إضافة حقل الصورة للتقارير 🚨🚨
    image = models.ImageField(upload_to='report_images/', verbose_name="صورة التقرير", blank=True, null=True)


    def __str__(self):
        return f"تقرير: {self.name} ({self.status})"

    class Meta:
        verbose_name = "تقرير باقة عاملة"
        verbose_name_plural = "تقارير الباقات العاملة"