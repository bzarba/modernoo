from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Brand, CarModel, Year, Product, Setting
import urllib.parse 

def home(request):
    brands = Brand.objects.all()
    settings = Setting.objects.first()
    return render(request, 'core/home.html', {'brands': brands, 'settings': settings})

def brands_list(request):
  brands = Brand.objects.all()
  return render(request, 'partials/brands.html', {'brands': brands})

def models_list(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    models = brand.models.all()  # Retrieve models associated with the brand
    context = {
        'brand': brand,
        'models': models,
    }
    return render(request, 'partials/models.html', context)

def years_list(request, brand_slug, model_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    model = get_object_or_404(CarModel, slug=model_slug, brand=brand)
    years = model.years.all()  # Retrieve years associated with the model
    context = {
        'brand': brand,
        'model': model,
        'years': years,
    }
    return render(request, 'partials/years.html', context)

def products_list(request, brand_slug, model_slug, year):
    # Retrieve the brand and model using slugs
    brand = get_object_or_404(Brand, slug=brand_slug)
    model = get_object_or_404(CarModel, slug=model_slug, brand=brand)

    # Retrieve the year using year_id
    year = get_object_or_404(Year, year=year, car_model=model)

    # Retrieve products for the given year
    products = Product.objects.filter(year=year)

    context = {
        'brand': brand,
        'model': model,
        'year': year,
        'products': products,
    }

    return render(request, 'core/products_list.html', context)



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    cart_item = cart.get(product_id)
    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else ''
        }

    request.session['cart'] = cart
    # return redirect('core:products_list', brand_slug=product.year.model.brand.slug, model_slug=product.year.model.slug, year=product.year.year)
    return HttpResponse('<button class="btn btn-neutral" disabled="true">Added</button>')

def cart(request):
    cart = request.session.get('cart', {})
    context = {
        'cart': cart,
    }
    return render(request, 'core/cart.html', context)

def remove_from_cart(request, product_id):
    product_id = str(product_id)
    cart = request.session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart

    return redirect('core:cart')

def update_cart(request, product_id):
    product_id = str(product_id)
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            del cart[product_id]
        else:
            cart[product_id]['quantity'] = quantity

    request.session['cart'] = cart
    return redirect('core:cart')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('core:cart')

    message_lines = ["Here are the products I want to order:"]
    for item in cart.values():
        line = f"{item['name']} - {item['quantity']} x ${item['price']}"
        message_lines.append(line)
    
    message = "\n".join(message_lines)
    telegram_base_url = "https://t.me/addisabeba7"
    params = {
        'url': '',  # Optional: add your website or product page URL here if needed
        'text': message
    }
    telegram_url = f"{telegram_base_url}?{urllib.parse.urlencode(params)}"
    return redirect(telegram_url)