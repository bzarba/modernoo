from django.contrib import admin
from .models import Brand, CarModel, Product, Setting, Option, Order, OrderItem
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
import csv

def download_invoice(modeladmin, request, queryset):
    """Generate and download an invoice for the selected orders."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="invoices.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Full Name', 'Address', 'City', 'Phone Number', 'Total Amount', 'Product', 'Quantity', 'Price', 'Options'])

    for order in queryset:
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            writer.writerow([order.id, order.fullname, order.address, order.city, order.phone_number, order.total_amount, item.product.name, item.quantity, item.price, item.options])

    return response

download_invoice.short_description = 'Download Invoice for selected Orders' 


# Unregister default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

# Customize the admin site
admin.site.name = 'Modernoo'
admin.site.site_header = 'Modernoo Administration'
admin.site.site_title = 'Modernoo'

admin.site.register(Option)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra empty forms
    readonly_fields = ('product', 'quantity', 'price', 'options')  # Read-only fields


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'address', 'city', 'phone_number', 'total_amount', 'state']
    actions = [download_invoice]
    inlines = [OrderItemInline]
    
    
    def get_queryset(self, request):
        """Filter orders to only show those with state 'order'."""
        qs = super().get_queryset(request)
        return qs.filter(state='order')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')
    search_fields = ('name',)  # Add a search field
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate the slug field based on the name

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    list_filter = ('brand',)  # Filter by brand
    search_fields = ('name',)  # Add a search field
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate the slug field based on the name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'car_model', 'price')
    list_filter = ('brand',)  # Filter by brand and car model
    search_fields = ('name', 'description')  # Add search fields
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate the slug field based on the name

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id')
    # search_fields = ('about_us', 'instagram_url', 'facebook_url', 'email')  # Add search fields
