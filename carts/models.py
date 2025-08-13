from django.db import models
from django.db.models.signals import pre_save

from store.models import Product, Variation
from shared.utils import unique_slug_generator#,unique_id_generator
from accounts.models import AppUser

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(blank=True, null=True,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

def cart_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        # instance.slug = unique_id_generator(instance)
        # print("This is the cart slug:",instance.slug)

pre_save.connect(cart_pre_save_receiver, sender=Cart)



class CartItem(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(blank=True, null=True,unique=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.slug

def cartitem_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(cartitem_pre_save_receiver, sender=CartItem)
