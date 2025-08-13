from django.urls import path 
from .views import carthome,add_to_cart,remove_cart,remove_cart_item, checkout

urlpatterns = [
    path('',carthome, name="cart"),
    path('add_cart/<int:product_id>/', add_to_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>', remove_cart_item, name='remove_cart_item'),

    path('checkout/', checkout, name='checkout'),
]
