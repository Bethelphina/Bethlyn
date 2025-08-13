from django.db import models
from django.urls import reverse
from accounts.models import UserProfile

# Create your models here.

class Vendor(models.Model):
    vendoruser = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    vendor_name = models.CharField(max_length=80, unique=True)
    vendor_email = models.EmailField(max_length=200, blank=True, default="vendor@bftt.com")
    address = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=20, blank=True, default='+23305000000')
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/categories', blank=True)
    description = models.TextField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "vendor"
        verbose_name_plural = "vendors"

    def get_vendor_url(self):
        return reverse("vendor_detail", args=[self.slug])

    def __str__(self):
        return self.vendor_name
