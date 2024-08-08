# store/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('cart/edit', views.edit_cart, name='edit_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_view, name='update_cart'),
    path('cart/items-number/', views.cart_items_count_view, name='cart_items_count_view'),
    path('checkout/', views.checkout, name='checkout'), 
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('brands/', views.brands_list, name='brands_list'),
    path('download-backup/', views.download_backup, name='download_backup'),
    path('get-car-models/<slug:brand_slug>/', views.get_car_models, name='get_car_models'),
    path('get-years/', views.get_years, name='get_years'),
    path('products/', views.products_list_desktop, name='products_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('<str:brand_slug>/', views.models_list, name='models_list'),
    path('<str:brand_slug>/<str:model_slug>/', views.years_list, name='years_list'),
    path('<str:brand_slug>/<str:model_slug>/<int:year>/', views.products_list, name='products_list'),
]
