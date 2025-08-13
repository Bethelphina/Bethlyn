from django.urls import path
from .views import place_order, payments,verify_payment,ordercompleted,paymentondelivery

urlpatterns = [
    path('place_order/', place_order, name='place_order'),
    path('payments/', payments, name='payments'),
    path('payondelivery/', paymentondelivery, name='payondelivery'),
    path('ordercompleted/', ordercompleted, name='order-completed'),

    # paystack config for urls
    path('payments/<str:ref>/', verify_payment, name='verify-payment')
    
]