from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product,Variation, ReviewRating,ProductGallery

# Register your models here.
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name","stock","price","category","is_available","is_featured","modified_on")
    prepopulated_fields = {"slug":('product_name',)}
    inlines = [ProductGalleryInline]
    # list_editable = ['stock','price','is_available',"is_featured"]


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product","variation_category","variation_value","is_active")
    list_editable = ('is_active',)
    list_filter=("product",'variation_value','variation_category')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)