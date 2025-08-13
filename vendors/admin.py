from django.contrib import admin
from .models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":('vendor_name',)}
    

admin.site.register(Vendor, VendorAdmin)