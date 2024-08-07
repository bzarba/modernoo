from django.db import models
from slugify import slugify
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from core.utils import generate_unique_slug

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
    name = models.CharField(max_length=255) # like color, size, type,
    choices = models.CharField(max_length=255, null=True) #separated by commas like red, blue, green
    
    def __str__(self):
        return self.name
    
    def get_choices_list(self):
        """Returns choices as a list."""
        return [choice.strip() for choice in self.choices.split(',')] if self.choices else []

    def set_choices_list(self, choices_list):
        """Sets choices from a list."""
        self.choices = ','.join(choice.strip() for choice in choices_list)
        self.save()

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    years = models.TextField(null=True, blank=True)  # Comma-separated years
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True)
    car_model = models.ForeignKey(CarModel, related_name='products', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default="", null=False, db_index=True)
    image = CloudinaryField(resource_type='image')
    options = models.ManyToManyField(Option)

    def save(self, *args, **kwargs):
        # Validate years
        if self.years:
            year_list = self.years.split(',')
            for year in year_list:
                if not year.strip().isdigit():
                    raise ValidationError(f"Invalid year: {year.strip()}")

        if not self.slug:
            self.slug = generate_unique_slug(self)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
# Orders
class Order(models.Model):
    STATE_CHOICES = [
        ('cart', 'Cart'),
        ('order', 'Order'),
    ]
    
    fullname = models.CharField(max_length=3000)
    address = models.TextField()
    city = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=30)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='cart')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    options = models.JSONField(default=dict)  # To store product options as 

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
