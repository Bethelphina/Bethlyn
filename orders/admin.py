from django.contrib import admin
from .models import Order,OrderProduct, Payment 

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','product','quantity','product_price','ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number",'status',"is_ordered","first_name","order_total",'email','phone')
    list_filter = ("is_ordered", "status",'phone')
    search_fields = ['order_number','status','first_name','phone']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)





class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order',"quantity","product","product_price")
    # pass
admin.site.register(OrderProduct,OrderProductAdmin)



class PaymentAdmin(admin.ModelAdmin):
    list_display = ("ref",'email','amount','verified')
    search_fields = ['ref','email','amount']


admin.site.register(Payment, PaymentAdmin)