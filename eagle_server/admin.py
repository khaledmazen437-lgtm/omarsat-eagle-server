from django.contrib import admin
from django import forms
from django.utils.html import format_html # للتأكد من وجود استدعاءات الـ HTML لو احتاج الأمر
from .models import ServerPlan, ServerNews, ServerReport
from django.contrib.admin import register

class ServerPlanAdminForm(forms.ModelForm):
    class Meta:
        model = ServerPlan
        fields = '__all__'
        widgets = {
            'features': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }

@register(ServerPlan)
class PlanAdmin(admin.ModelAdmin):
    form = ServerPlanAdminForm

    list_display = ('name', 'server_type', 'price', 'duration')
    list_filter = ('server_type',)
    list_editable = ('server_type', 'price', 'duration')

    search_fields = ('name', 'features')

    fieldsets = (
        ('تفاصيل الخدمة', {

            'fields': ('name', 'server_type', 'price', 'duration', 'image')
        }),
        ('المميزات والتفاصيل', {
            'fields': ('features',)
        }),
    )

@register(ServerNews)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title', 'content')
    ordering = ('-date_posted',)

@register(ServerReport)
class ServerReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'last_updated')
    list_filter = ('status',)
    search_fields = ('name', 'report_details')

    fieldsets = (
        ('حالة الباقة', {

            'fields': ('name', 'status', 'image')
        }),
        ('تفاصيل التقرير والمتابعة', {'fields': ('report_details',)}),
    )
