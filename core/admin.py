# store/admin.py
from django.contrib import admin
from .models import Brand, CarModel, Year, Product, Setting
from django.contrib.auth.models import  User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.name = 'Modernoo'
admin.site.site_header = 'Modernoo Adminstration'
admin.site.site_header = 'Modernoo Adminstration'
admin.site.site_title = 'Modernoo'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')


admin.site.register(CarModel)
admin.site.register(Year)
admin.site.register(Product)
admin.site.register(Setting)