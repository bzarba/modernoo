from django.db import models
# from django.utils.text import slugify
from slugify import slugify
from cloudinary.models import CloudinaryField
import cloudinary.api
import cloudinary.uploader

# slugifyer = Slugify()

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
from django.db import models

class Year(models.Model):
    year = models.IntegerField()
    image = CloudinaryField(resource_type='image')
    car_model = models.ForeignKey('CarModel', related_name='years', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.year} - {self.car_model}'

class Option(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.ForeignKey(Year, related_name='products', on_delete=models.CASCADE)
    # options = models.ManyToManyField(Option, related_name='options', blank=True, null=True)
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
    complete= models.BooleanField(default=False)

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
    home_video = CloudinaryField(resource_type='video')
