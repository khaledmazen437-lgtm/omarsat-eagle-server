from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from urllib.parse import quote
from .models import Product, Review, Order, OrderItem, Cart, CartItem, ChannelFile, Wishlist, HomeBanner, TutorialVideo

from .models import Product, Review, Order, OrderItem, Cart, CartItem, ChannelFile, Wishlist, HomeBanner

from eagle_server.models import ServerPlan, ServerNews, ServerReport

def _cart_id(request):
    """جلب أو إنشاء رقم تعريفي للجلسة (Session ID) للزائر"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def get_user_cart_items(request):
    """دالة موحدة لجلب عناصر السلة للمستخدم المسجل أو الزائر"""
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user, is_active=True)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            return CartItem.objects.filter(cart=cart, is_active=True)
        except (Cart.DoesNotExist, ObjectDoesNotExist):
            return CartItem.objects.none()

def home_view(request):
    try:
        active_banners = HomeBanner.objects.filter(is_active=True).order_by('ordering')
    except:
        active_banners = []

    context = {
        'banners': active_banners
    }
    return render(request, 'index.html', context)

def store_view(request):
    products = Product.objects.all()

    try:
        active_banners = HomeBanner.objects.filter(is_active=True).order_by('ordering')

    except:
        active_banners = []

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category__icontains=category_id)

    context = {
        'products': products,

        'banners': active_banners,
    }

    return render(request, 'store.html', context)

def channel_files_center_view(request):
    try:

        all_channel_files = ChannelFile.objects.all().order_by('-date_added')
    except:
        all_channel_files = []

    context = {
        'channel_files': all_channel_files,
        'page_title': 'مركز ملفات القنوات والسوفت وير'
    }

    return render(request, 'channel_files_center.html', context)

def discounts_view(request):
    discounted_products = Product.objects.filter(discount_price__isnull=False).order_by('name')

    context = {'products': discounted_products, 'page_title': 'منتجات عليها خصم'}
    return render(request, 'store.html', context)

def server_view(request):
    iptv_plans = ServerPlan.objects.filter(server_type='iptv')
    cccam_plans = ServerPlan.objects.filter(server_type='cccam')

    working_packages = ServerReport.objects.all().order_by('name')
    latest_news = ServerNews.objects.all().order_by('-date_posted')

    return render(request, 'server.html', {
        'iptv_plans': iptv_plans,
        'cccam_plans': cccam_plans,
        'working_packages': working_packages,
        'news_list': latest_news
    })

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_details.html', {'product': product})

def channel_file_details(request, id):
    file = get_object_or_404(ChannelFile, id=id)
    return render(request, 'channel_file_details.html', {'file': file})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    current_user = request.user

    if current_user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(product=product, quantity=1, user=current_user)

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(product=product, quantity=1, cart=cart)

    messages.success(request, f"{product.name} تمت إضافته للسلة!")
    return redirect('cart')

def increase_quantity(request, product_id):
    if request.user.is_authenticated:
        query_filter = Q(user=request.user, product_id=product_id)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            query_filter = Q(cart=cart, product_id=product_id)
        except Cart.DoesNotExist:
            return redirect('cart')

    try:
        cart_item = CartItem.objects.get(query_filter)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def decrease_quantity(request, product_id):
    if request.user.is_authenticated:
        query_filter = Q(user=request.user, product_id=product_id)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            query_filter = Q(cart=cart, product_id=product_id)
        except Cart.DoesNotExist:
            return redirect('cart')

    try:
        cart_item = CartItem.objects.get(query_filter)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(product_id=product_id, user=request.user).delete()
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            CartItem.objects.filter(product_id=product_id, cart=cart).delete()
        except Cart.DoesNotExist:
            pass

    messages.info(request, "تم حذف المنتج من السلة.")
    return redirect('cart')

def cart_view(request):
    cart_items = get_user_cart_items(request)

    total = Decimal('0.00')
    total_shipping = Decimal('0.00')

    for cart_item in cart_items:
        price = Decimal(cart_item.product.discount_price if cart_item.product.discount_price else cart_item.product.price)
        shipping = Decimal(cart_item.product.shipping_fee)

        total += price * cart_item.quantity
        total_shipping += shipping * cart_item.quantity

    tax = Decimal('0.00')
    grand_total = total + total_shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': total,
        'shipping_fee': total_shipping,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)

def checkout(request):
    cart_items = get_user_cart_items(request)

    if not cart_items or len(cart_items) == 0:
        messages.warning(request, "السلة فارغة يا صديقي! ضيف منتجات الأول 🛒")
        return redirect('store')

    if not request.user.is_authenticated:
        messages.error(request, "يجب تسجيل الدخول لإتمام الطلب.")
        return redirect(f'/login/?next={request.path}')

    total = sum(Decimal(item.product.discount_price if item.product.discount_price else item.product.price) * item.quantity for item in cart_items)
    shipping_fee = sum(Decimal(item.product.shipping_fee) * item.quantity for item in cart_items)
    tax = Decimal('0.00')
    grand_total = total + shipping_fee + tax

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_input = request.POST.get('address')
        city = request.POST.get('city')
        payment_method = request.POST.get('payment_method')
        payment_screenshot = request.FILES.get('receiptImage')

        try:
            new_order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone_number=phone,
                address=f"{city} - {address_input}",
                total_price=grand_total,
                payment_method=payment_method,
                payment_screenshot=payment_screenshot,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            is_subscription = False
            for item in cart_items:
                if hasattr(item.product, 'is_subscription') and item.product.is_subscription:
                    is_subscription = True
                    break

            if is_subscription:
                new_order.is_server_plan = True
                new_order.expiry_date = date.today() + timedelta(days=365)
                new_order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.discount_price if item.product.discount_price else item.product.price,
                    user=request.user
                )

            cart_items.delete()

            # --- توليد رابط واتساب للإشعار (WhatsApp Notification) ---
            payment_method_name = dict(Order.PAYMENT_METHODS).get(payment_method, payment_method)

            screenshot_link = ""
            if new_order.payment_screenshot:
                screenshot_link = f"\n\n*اضغط هنا لرؤية صورة الإثبات فوراً:*\n{request.build_absolute_uri(new_order.payment_screenshot.url)}"

            wa_message = (
                f"✅ طلب جديد رقم #{new_order.id}\n"
                f"--------------------------\n"
                f"👤 العميل: {full_name}\n"
                f"📞 الهاتف: {phone}\n"
                f"💰 الإجمالي: {grand_total} ج.م\n"
                f"💳 طريقة الدفع: {payment_method_name}\n"
                f"--------------------------\n"
                f"🛑 رجاء مراجعة الطلب رقم {new_order.id} 🛑\n"
                f"لتأكيد استلام المبلغ المُحول.\n"
                f"{screenshot_link}"
            )

            ADMIN_WA_NUMBER = "+201011058982"

            encoded_message = quote(wa_message)
            wa_url = f"https://wa.me/{ADMIN_WA_NUMBER}?text={encoded_message}"

            request.session['wa_redirect_url'] = wa_url

            messages.success(request, "تم استلام طلبك بنجاح! سيتم تحويلك إلى الواتساب لتأكيد الإشعار.")
            return redirect('profile')

        except Exception as e:
            print(f"❌ خطأ قاتل عند حفظ الطلب: {e}")
            messages.error(request, f"حدث خطأ أثناء حفظ الطلب. (السبب: {e})")
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'total': total,
        'shipping_fee': shipping_fee,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    context = {'wishlist_items': wishlist_items}
    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()
        messages.success(request, f'{product.name} تم إزالته من المفضلة.')
    else:
        messages.success(request, f'{product.name} تمت إضافته إلى المفضلة.')

    return redirect(request.META.get('HTTP_REFERER', 'store'))

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'كلمة المرور وتأكيدها غير متطابقين.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'البريد الإلكتروني مسجل مسبقاً.')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        pass_word = request.POST.get('password')

        user = authenticate(request, username=username, password=pass_word)

        if user is not None:
            login(request, user)
            messages.success(request, f"مرحباً بك مجدداً يا {username}!")

            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور خطأ ❌")

    return render(request, 'login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    wa_redirect_url = request.session.pop('wa_redirect_url', None)

    if wa_redirect_url:
        return redirect(wa_redirect_url)

    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': user_orders})

@login_required(login_url='login')
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating_value = request.POST.get('rating')
        comment_text = request.POST.get('comment')

        if Review.objects.filter(user=request.user, product=product).exists():
            messages.error(request, "لقد قمت بتقييم هذا المنتج بالفعل.")
            return redirect('product_details', id=product_id)

        Review.objects.create(
            user=request.user,
            product=product,
            rating=int(rating_value),
            comment=comment_text,
        )
        messages.success(request, "تم إضافة تقييمك بنجاح! شكراً لك.")

    return redirect('product_details', id=product_id)

def about_us_view(request):
    return redirect('home')

def contact_us_view(request):
    return redirect('home')

def search_view(request):
    query = request.GET.get('q', '').strip()
    products = []
    iptv_plans = []
    cccam_plans = []

    if query:
        keyword_map = {
            'رسيفر': 'receiver', 'ريسيفر': 'receiver', 'رسيفير': 'receiver', 'ريسفير': 'receiver', 'رسفر': 'receiver', 'جهاز': 'receiver',
            'عدس': 'lnb', 'قطعة': 'lnb', 'لاقط': 'lnb', 'طبق': 'lnb', 'اطباق': 'lnb', 'دش': 'lnb',
            'كابل': 'cable', 'سلك': 'cable', 'وصل': 'cable', 'hdmi': 'cable', 'usb': 'cable',
            'ريموت': 'remote', 'رموت': 'remote', 'تحكم': 'remote',
            'صيان': 'maintenance', 'اكسسوار': 'accessories', 'تركيب': 'tools', 'ادوات': 'tools',
            'iptv': 'iptv', 'cccam': 'cccam', 'شير': 'cccam', 'شيرينج': 'cccam',
        }

        target_codes = []
        for word, code in keyword_map.items():
            if word in query.lower():
                target_codes.append(code)

        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(category__in=target_codes)
        ).distinct()

        all_plans = ServerPlan.objects.filter(
            Q(name__icontains=query) | Q(features__icontains=query) |
            Q(server_type__icontains=query)
        ).distinct()

        iptv_plans = all_plans.filter(server_type='iptv')
        cccam_plans = all_plans.filter(server_type='cccam')

    context = {
        'query': query,
        'products': products,
        'iptv_plans': iptv_plans,
        'cccam_plans': cccam_plans,
    }

    return render(request, 'search_results.html', context)

# في ملف store/views.py
# ... (بعد دالة channel_files_center_view)

def tutorials_view(request):
    # تأكد من استيراد TutorialVideo في بداية الملف (from .models import ..., TutorialVideo)
    try:
        videos = TutorialVideo.objects.filter(is_active=True).order_by('-date_added')
    except NameError:
        # إذا لم يتم استيراد TutorialVideo في بداية الملف، سيعطي خطأ
        # لكن لو تم الاستيراد، سيتم تجاهل هذا الجزء
        videos = []

    context = {
        'videos': videos,
        'page_title': 'شروحات وتطبيقات بالفيديو'
    }

    return render(request, 'tutorials.html', context)
