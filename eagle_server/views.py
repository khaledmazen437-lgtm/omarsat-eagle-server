from django.shortcuts import render
# 🚨 تأكد من استيراد ServerReport من الملف الصحيح
from eagle_server.models import ServerPlan, ServerNews, ServerReport 
# أو من .models لو كانت في نفس المكان

def server_view(request):
    # فلترة الباقات حسب النوع (المبيعات)
    iptv_plans = ServerPlan.objects.filter(server_type='iptv')
    cccam_plans = ServerPlan.objects.filter(server_type='cccam')
    
    # 🚨🚨 FIX: جلب التقارير من نموذج ServerReport الجديد (بيانات الحالة)
    working_packages = ServerReport.objects.all().order_by('name')
    
    # جلب الأخبار الأحدث أولاً
    latest_news = ServerNews.objects.all().order_by('-date_posted')
    
    return render(request, 'server.html', {
        'iptv_plans': iptv_plans,
        'cccam_plans': cccam_plans,
        # الآن working_packages ستحتوي على حالة السيرفر وتفاصيل التقرير
        'working_packages': working_packages, 
        'news_list': latest_news, 
    })