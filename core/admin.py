from django.contrib import admin
from .models import Brand, CarModel, Product, Setting, Option
from django.contrib.auth.models import User, Group

# Unregister default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

# Customize the admin site
admin.site.name = 'Modernoo'
admin.site.site_header = 'Modernoo Administration'
admin.site.site_title = 'Modernoo'

admin.site.register(Option)

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
