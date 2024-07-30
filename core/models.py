from django.db import models
from slugify import slugify
from cloudinary.models import CloudinaryField

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = CloudinaryField(resource_type='image')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, related_name='models', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CarModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Option(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    years = models.TextField(null=True, blank=True)  # Allow null values and blank fields
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True)
    car_model = models.ForeignKey(CarModel, related_name='products', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default="", null=False, db_index=True)
    image = CloudinaryField(resource_type='image')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Orders
class Order(models.Model):
    fullname = models.CharField(max_length=3000)
    address = models.TextField()
    city = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=30)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True)
    options = models.TextField()
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)

class Setting(models.Model):
    active = models.BooleanField(default=False)
    home_video = CloudinaryField(resource_type='video')
    about_us = models.TextField(null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    wechat_id = models.CharField(max_length=255, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f'Setting {self.id}'
