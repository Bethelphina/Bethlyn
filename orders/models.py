from django.db import models
from accounts.models import AppUser
from store.models import Product,Variation
from django.db.models.signals import pre_save
from shared.utils import unique_order_generator


# Paystack payment
from .paystack import Paystack
import secrets

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    ref = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(default=0.00)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return f'payment : {self.ref}'


    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(20)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref 
        super().save(*args,**kwargs)

    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status,result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True 
            self.save()
        if self.verified:
            return True 
        return False 


class Order(models.Model):
    STATUS = (
        ('New', "New"),
        ('Accepted', "Accepted"),
        ('Completed', "Completed"),
        ('Cancelled', "Cancelled"),
    )
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=70)
    email = models.EmailField()
    phone = models.CharField(max_length=18)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    # city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=500, help_text='Additional Info', blank=True, null=True)
    order_number = models.SlugField(blank=True, null=True,unique=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def fulladdress(self):
        return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.order_number



def order_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.order_number:
        instance.order_number = unique_order_generator(instance)

pre_save.connect(order_pre_save_receiver, sender=Order)




class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
