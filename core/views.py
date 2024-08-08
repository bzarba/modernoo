# views.py

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core import management
from django.conf import settings
from datetime import datetime
import os

from .models import Brand, CarModel, Product, Order, OrderItem
from .cart import get_or_create_cart_order, add_to_cart, remove_from_cart, update_cart, get_cart_items, get_cart_item_count


def home(request):
    """Render the home page with a list of brands."""
    brands = Brand.objects.all()
    return render(request, 'core/home.html', {'brands': brands})


def brands_list(request):
    """Render a list of brands."""
    brands = Brand.objects.all()
    return render(request, 'partials/brands.html', {'brands': brands})


def models_list(request, brand_slug):
    """Render a list of car models for a given brand."""
    brand = get_object_or_404(Brand, slug=brand_slug)
    models = brand.models.all()
    return render(request, 'partials/models.html', {'brand': brand, 'models': models})


def years_list(request, brand_slug, model_slug):
    """Render a list of years for a given brand and model."""
    brand = get_object_or_404(Brand, slug=brand_slug)
    model = get_object_or_404(CarModel, slug=model_slug, brand=brand)
    
    current_year = datetime.now().year
    years = list(range(1990, current_year + 1))
    years.reverse()

    return render(request, 'partials/years.html', {'brand': brand, 'model': model, 'years': years})


def products_list(request, brand_slug, model_slug, year):
    """Render a list of products for a given brand, model, and year."""
    brand = get_object_or_404(Brand, slug=brand_slug)
    model = get_object_or_404(CarModel, slug=model_slug, brand=brand)
    
    products = Product.objects.filter(car_model=model, years__contains=str(year))

    return render(request, 'core/products_list.html', {
        'brand': brand,
        'model': model,
        'year': year,
        'products': products
    })


def edit_cart(request):
    """Add or update an item in the cart."""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        options = {key: value for key, value in request.POST.items() if key.startswith('option_')}
        
        add_to_cart(request, product_id, quantity, options)

        messages.success(request, 'Added Successfully')
        # print(12)

        cart_item_count = get_cart_item_count(request)
        print(cart_item_count)
        return render(request, 'partials/cart_number.html', {'cart_item_count': cart_item_count})

def cart(request):
    """Render the cart page with items."""
    print(get_cart_items(request))
    cart_items = get_cart_items(request)
    return render(request, 'core/cart.html', {'cart': cart_items})


def remove_from_cart_view(request, product_id):
    """Remove an item from the cart."""
    remove_from_cart(request, product_id)
    return redirect('core:cart')


def update_cart_view(request, product_id):
    """Update the quantity of an item in the cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        update_cart(request, product_id, quantity)

    return redirect('core:cart')

def cart_items_count_view(request):
    print('c',get_cart_item_count(request))
    return HttpResponse(get_cart_item_count(request))

def checkout(request):
    """Handle checkout process and finalize the order."""
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        city = request.POST.get('city', '')
        phone_number = request.POST.get('phone_number')
        
        cart_order = get_or_create_cart_order(request)
        if not cart_order:
            return redirect('core:cart')

        order = Order.objects.create(
            fullname=fullname,
            address=address,
            city=city,
            phone_number=phone_number,
            complete=False,
            state='order'
        )

        total_amount = 0
        for item in OrderItem.objects.filter(order=cart_order):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
                options=item.options
            )
            total_amount += item.product.price * item.quantity

        order.total_amount = total_amount
        order.save()

        cart_order.delete()

        messages.success(request, 'Order placed successfully!')
        return redirect('core:order_confirmation', order_id=order.id)

    return render(request, 'core/checkout.html')


def download_backup(request):
    """Generate and download a backup of the database."""
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    db_backup_file = os.path.join(backup_dir, 'backup.json')

    management.call_command('dumpdata', '--output', db_backup_file)
    
    if os.path.exists(db_backup_file):
        with open(db_backup_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename=backup.json'
            return response
    else:
        return HttpResponse("Backup file not found", status=404)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'core/order_confirmation.html', {'order': order})