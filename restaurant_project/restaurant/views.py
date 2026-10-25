from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Category, CustomerProfile, MenuItem, Order, OrderItem, Reservation
from .forms import CheckoutForm, MenuItemForm, ReservationForm, SignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to TastyBite! Your points balance starts at 0.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'restaurant/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            CustomerProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect(request.GET.get('next') or 'home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'restaurant/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def account_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = request.user.orders.prefetch_related('items__menu_item').order_by('-created_at')[:10]
    return render(request, 'restaurant/account.html', {'profile': profile, 'orders': orders})

def home_view(request):
    categories = Category.objects.all()
    popular_items = MenuItem.objects.filter(is_popular=True)[:6]
    chef_specials = MenuItem.objects.order_by('-rating')[:4]

    # Drinks showcase (Craft Drinks + Hot Beverages + Fresh Juices)
    drinks_items = MenuItem.objects.filter(
        category__name__in=['Craft Drinks', 'Hot Beverages', 'Fresh Juices']
    ).order_by('-rating')[:8]

    # Desserts showcase
    desserts_items = MenuItem.objects.filter(
        category__name='Heavenly Desserts'
    ).order_by('-rating')[:6]

    # Calculate stats
    stats = {
        'items_count': MenuItem.objects.count(),
        'happy_customers': '15,000+',
        'avg_rating': '4.9 ★',
        'delivery_mins': '30 Min'
    }

    context = {
        'categories': categories,
        'popular_items': popular_items,
        'chef_specials': chef_specials,
        'drinks_items': drinks_items,
        'desserts_items': desserts_items,
        'stats': stats
    }
    return render(request, 'restaurant/home.html', context)


def menu_view(request):
    categories = Category.objects.all()
    items = MenuItem.objects.all()
    
    # Search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) | 
            Q(name_ar__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(description_ar__icontains=search_query)
        )

    # Category filter
    category_id = request.GET.get('category', '').strip()
    if category_id:
        items = items.filter(category_id=category_id)

    # Dietary / Flag filter
    dietary = request.GET.get('dietary', '').strip()
    if dietary == 'spicy':
        items = items.filter(is_spicy=True)
    elif dietary == 'vegetarian':
        items = items.filter(is_vegetarian=True)
    elif dietary == 'popular':
        items = items.filter(is_popular=True)

    # Sorting
    sort_by = request.GET.get('sort', '').strip()
    if sort_by == 'price_low':
        items = items.order_by('price')
    elif sort_by == 'price_high':
        items = items.order_by('-price')
    elif sort_by == 'rating':
        items = items.order_by('-rating')
    elif sort_by == 'prep_time':
        items = items.order_by('prep_time_mins')

    context = {
        'categories': categories,
        'items': items,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_dietary': dietary,
        'selected_sort': sort_by,
    }
    return render(request, 'restaurant/menu.html', context)


def item_detail_view(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    related_items = MenuItem.objects.filter(category=item.category).exclude(pk=pk)[:3]
    context = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'restaurant/item_detail.html', context)


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            subtotal = float(item.price) * quantity
            total_price += subtotal
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except MenuItem.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'restaurant/cart.html', context)


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty! / سلة التسوق فارغة!")
        return redirect('menu')

    cart_items = []
    total_price = 0
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            subtotal = float(item.price) * quantity
            total_price += subtotal
            cart_items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
        except MenuItem.DoesNotExist:
            continue

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user if request.user.is_authenticated else None
                order.total_price = total_price
                order.status = 'PENDING'
                order.save()

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        menu_item=cart_item['item'],
                        quantity=cart_item['quantity'],
                        price=cart_item['item'].price
                    )

                if request.user.is_authenticated:
                    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
                    profile.points += int(total_price // 10)
                    profile.save(update_fields=['points'])
                    order.points_awarded = True
                    order.save(update_fields=['points_awarded'])

            request.session['cart'] = {}
            messages.success(request, f"Order #{order.id} placed successfully! / تم تقديم طلبك بنجاح!")
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, "Please correct the errors below and try again. / يرجى تصحيح الأخطاء أدناه.")
    else:
        form = CheckoutForm()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }
    return render(request, 'restaurant/checkout.html', context)


def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'restaurant/order_success.html', {'order': order})


def track_order_view(request):
    order = None
    search_query = request.GET.get('order_query', '').strip()
    if search_query:
        if search_query.isdigit():
            order = Order.objects.filter(id=search_query).first()
        if not order:
            order = Order.objects.filter(phone=search_query).first()
        if not order:
            messages.warning(request, "No order found matching your query. / لم نتمكن من العثور على طلب برقم الهاتف أو الرقم المرجعي المدخل.")
            
    return render(request, 'restaurant/track_order.html', {'order': order, 'search_query': search_query})


def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.status = 'CONFIRMED'
            reservation.save()
            messages.success(
                request,
                f"Table reserved successfully for {reservation.customer_name} on "
                f"{reservation.reservation_date} at {reservation.reservation_time}! / تم حجز الطاولة بنجاح!"
            )
            return redirect('reservation_success', reservation_id=reservation.id)
        else:
            messages.error(request, "Please correct the errors below and try again. / يرجى تصحيح الأخطاء أدناه.")
    else:
        form = ReservationForm()

    return render(request, 'restaurant/reservation.html', {'form': form})


def reservation_success_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'restaurant/reservation_success.html', {'reservation': reservation})


def kitchen_dashboard_view(request):
    orders = Order.objects.prefetch_related('items__menu_item').all().order_by('-created_at')
    reservations = Reservation.objects.all().order_by('-created_at')[:10]
    
    status_filter = request.GET.get('status', 'ALL')
    if status_filter != 'ALL':
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'reservations': reservations,
        'selected_status': status_filter,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'restaurant/kitchen_dashboard.html', context)


@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        if new_status == 'DELIVERED':
            order.is_completed = True
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}")
    
    return redirect('kitchen_dashboard')


# Cart Management Functions (Traditional & AJAX)
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    str_id = str(item_id)
    cart[str_id] = cart.get(str_id, 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Added item to cart! / تم إضافة الوجبة إلى السلة.")
    return redirect(request.META.get('HTTP_REFERER', 'menu'))


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    str_id = str(item_id)
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
    return redirect('cart')


def update_cart_quantity(request, item_id, action):
    cart = request.session.get('cart', {})
    str_id = str(item_id)
    if str_id in cart:
        if action == 'increase':
            cart[str_id] += 1
        elif action == 'decrease':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
        request.session['cart'] = cart
    return redirect('cart')


# AJAX API Endpoints for Slide-over Cart
@require_POST
def add_to_cart_ajax(request, item_id):
    cart = request.session.get('cart', {})
    str_id = str(item_id)
    cart[str_id] = cart.get(str_id, 0) + 1
    request.session['cart'] = cart
    
    total_count = sum(cart.values())
    item = get_object_or_404(MenuItem, id=item_id)
    
    return JsonResponse({
        'success': True,
        'message': f"Added '{item.name}' to cart!",
        'cart_count': total_count,
        'cart_items': _get_cart_data(cart)
    })

@require_POST
def update_cart_ajax(request, item_id):
    cart = request.session.get('cart', {})
    str_id = str(item_id)
    action = request.POST.get('action', 'increase')
    
    if str_id in cart:
        if action == 'increase':
            cart[str_id] += 1
        elif action == 'decrease':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
        request.session['cart'] = cart

    return JsonResponse({
        'success': True,
        'cart_count': sum(cart.values()),
        'cart_items': _get_cart_data(cart)
    })

def get_cart_ajax(request):
    cart = request.session.get('cart', {})
    return JsonResponse({
        'cart_count': sum(cart.values()),
        'cart_items': _get_cart_data(cart)
    })


def _get_cart_data(cart):
    cart_items = []
    total_price = 0
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            subtotal = float(item.price) * quantity
            total_price += subtotal
            cart_items.append({
                'id': item.id,
                'name': item.name,
                'name_ar': item.name_ar or item.name,
                'price': float(item.price),
                'quantity': quantity,
                'subtotal': subtotal,
                'image': item.display_image
            })
        except MenuItem.DoesNotExist:
            continue
    return {'items': cart_items, 'total_price': total_price}


# ---------------------------------------------------------------------------
# Menu Item CRUD (Create, Read, Update, Delete) — staff only.
# Read is already covered by menu_view / item_detail_view for everyone.
# ---------------------------------------------------------------------------

@staff_member_required
def manage_items_view(request):
    """List all menu items with quick links to edit or delete them (Read + entry point for Update/Delete)."""
    items = MenuItem.objects.select_related('category').all().order_by('category__order', 'name')
    return render(request, 'restaurant/manage_items.html', {'items': items})


@staff_member_required
def add_item_view(request):
    """Create a new menu item."""
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Dish added successfully! / تم إضافة الوجبة بنجاح!")
            return redirect('manage_items')
        else:
            messages.error(request, "Please correct the errors below. / يرجى تصحيح الأخطاء أدناه.")
    else:
        form = MenuItemForm()

    return render(request, 'restaurant/add_item.html', {'form': form, 'is_edit': False})


@staff_member_required
def edit_item_view(request, pk):
    """Update an existing menu item."""
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{item.name}' updated successfully! / تم تعديل الوجبة بنجاح!")
            return redirect('manage_items')
        else:
            messages.error(request, "Please correct the errors below. / يرجى تصحيح الأخطاء أدناه.")
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'restaurant/add_item.html', {'form': form, 'is_edit': True, 'item': item})


@staff_member_required
def delete_item_view(request, pk):
    """Delete a menu item (confirmation required via POST)."""
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f"'{item_name}' was deleted. / تم حذف الوجبة.")
        return redirect('manage_items')

    return render(request, 'restaurant/delete_item_confirm.html', {'item': item})