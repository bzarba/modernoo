# core/cart.py

from django.shortcuts import get_object_or_404
from .models import Product, Order, OrderItem
from django.db.models import Sum
import json

def get_or_create_cart_order(request):
    """Retrieve or create a cart order based on session."""
    session_cart_id = request.session.get('cart_id')
    
    if session_cart_id:
        try:
            return Order.objects.get(id=session_cart_id, state='cart')
        except Order.DoesNotExist:
            # Cart ID exists but no matching cart found, create a new one
            return create_cart_order(request)
    else:
        return create_cart_order(request)

def create_cart_order(request):
    """Create a new cart order and save its ID in the session."""
    cart_order = Order.objects.create(
        fullname='Temporary Cart',
        address='',
        city='',
        phone_number=''
    )
    request.session['cart_id'] = cart_order.id
    return cart_order

def add_to_cart(request, product_id, quantity, options):
    """Add or update an item in the cart."""
    product = get_object_or_404(Product, pk=product_id)
    cart_order = get_or_create_cart_order(request)

    # Serialize options to a string to ensure uniqueness
    options_str = json.dumps(options, sort_keys=True)

    cart_item, created = OrderItem.objects.get_or_create(
        order=cart_order,
        product=product,
        options=options_str,
        defaults={'quantity': int(quantity), 'price': product.price}
    )

    if not created:
        cart_item.quantity += int(quantity)
    cart_item.save()

def remove_from_cart(request, product_id):
    """Remove an item from the cart."""
    cart_order = get_or_create_cart_order(request)
    OrderItem.objects.filter(order=cart_order, product_id=product_id).delete()

def update_cart(request, product_id, quantity):
    """Update the quantity of an item in the cart."""
    cart_order = get_or_create_cart_order(request)
    cart_item = OrderItem.objects.filter(order=cart_order, product_id=product_id).first()
    
    if cart_item:
        if int(quantity) < 1:
            cart_item.delete()
        else:
            cart_item.quantity = int(quantity)
            cart_item.save()

def get_cart_items(request):
    """Get all items in the cart."""
    cart_order = get_or_create_cart_order(request)
    cart_items = OrderItem.objects.filter(order=cart_order)
    for item in cart_items:
        item.options = json.loads(item.options)
    return cart_items

def get_cart_item_count(request):
    """Get the total number of items in the cart."""
    return get_cart_items(request).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
