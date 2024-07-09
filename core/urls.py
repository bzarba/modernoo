# store/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'), 
    path('brands/', views.brands_list, name='brands_list'),
    path('<str:brand_slug>/', views.models_list, name='models_list'),
    path('<str:brand_slug>/<str:model_slug>/', views.years_list, name='years_list'),
    path('<str:brand_slug>/<str:model_slug>/<int:year>/', views.products_list, name='products_list'),
]
