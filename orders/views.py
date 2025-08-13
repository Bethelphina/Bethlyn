from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from carts.models import CartItem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
from store.models import Product

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import datetime

# Create your views here.
def place_order(request, total=0,quantity = 0):
    current_user  = request.user

    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect('store')

    # total and tax calculation
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = 0 #(17.5 * total) / 100
    grand_total = total + tax

    
    # Storing all billing information into order table or model
    if request.method == "POST":

        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name  = form.cleaned_data["last_name"]
            data.email  = form.cleaned_data["email"]
            data.phone  = form.cleaned_data["phone"]
            data.address_line_1  = form.cleaned_data["address_line_1"]
            data.address_line_2  = form.cleaned_data["address_line_2"]
            # data.city  = form.cleaned_data["city"]
            data.order_note  = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax 
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()        

            order_number = data.order_number

            order = Order.objects.get(user = current_user, is_ordered=False, order_number=order_number)
            context = {
                "order":order,
                "cart_items":cart_items,
                "total":total,
                'tax':tax,
                'grand_total':grand_total,
                }

            return render(request,"orders/payments.html", context)
    else:
        return redirect("checkout")



def payments(request):
    # lastorderbyuser=Order.objects.latest('slug').order_number
    # lastorderbyuser=Order.objects.latest(request.user.email).order_number
    lastorderbyuser=Order.objects.latest('user').order_number
    order = Order.objects.get(user=request.user, is_ordered=False, order_number = lastorderbyuser)
    print(order)
    payment = Payment(
        user = request.user,
        email = request.user.email,
        amount = order.order_total
    )
    payment.save()
    order.payment = payment
    order.is_ordered=True
    order.save()

    # move the cart item to order product table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # adding variations to orderproduct
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # reducing stock quantity
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clearing the cart after order completion
    CartItem.objects.filter(user=request.user).delete()

    return render (request, 'orders/confirmpayment.html', {'payment':payment, "paystack_publick_key":settings.PAYSTACK_TEST_PUBLIC_KEY})





def paymentondelivery(request):
    # lastorderbyuser=Order.objects.latest('slug').order_number
    # lastorderbyuser=Order.objects.latest(request.user.email).order_number
    lastorderbyuser=Order.objects.latest('user').order_number
    order = Order.objects.get(user=request.user, is_ordered=False, order_number = lastorderbyuser)

    payment = Payment(
        user = request.user,
        email = request.user.email,
        amount = order.order_total
    )
    payment.save()
    order.payment = payment
    order.is_ordered=True
    order.save()

    # move the cart item to order product table
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # adding variations to orderproduct
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # reducing stock quantity
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clearing the cart after order completion
    CartItem.objects.filter(user=request.user).delete()

    # sending order info to completed screen and sending email to customer
    order = Order.objects.get(user=request.user, is_ordered=True, order_number = lastorderbyuser)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)

    subtotal = 0
    for i in ordered_products:
        subtotal += i.product_price * i.quantity

    # ORDER COMPLETED EMAIL
    email_subject = "Thank you for your Order"
    email_message = render_to_string('orders/pod.html',{
        "user":request.user,
        "order":order,
        'payment':payment
    })    
    customer_email = request.user.email
    send_email = EmailMessage(email_subject, email_message, to=[customer_email])
    send_email.send()

    context = {
        'order_number':order.order_number,
        'ordered_date':order.created_at,
        'order': order,
        'payment':payment,
        'ordered_products':ordered_products,
        'subtotal':subtotal
    }
    return render(request,'orders/pod_completed.html',context)

    # return render (request, 'orders/order_complete.html', {'payment':payment})




def ordercompleted(request):
    return render(request, 'orders/order_complete.html')



def verify_payment(request, ref):
    payment = get_object_or_404(Payment,ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification successful")

        # sending order info to completed screen and sending email to customer
        lastorderbyuser=Order.objects.latest('user').order_number
        order = Order.objects.get(user=request.user, is_ordered=True, order_number = lastorderbyuser)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        # ORDER COMPLETED EMAIL
        email_subject = "Thank you for your Order"
        email_message = render_to_string('orders/order_received.html',{
            "user":request.user,
            "order":order,
            'payment':payment
        })    
        customer_email = request.user.email
        send_email = EmailMessage(email_subject, email_message, to=[customer_email])
        send_email.send()

        context = {
            'order_number':order.order_number,
            'ordered_date':order.created_at,
            'order': order,
            'paymentId':payment.ref,
            'ordered_products':ordered_products,
            'subtotal':subtotal
        }
        return render(request,'orders/order_complete.html',context)
        # End of sending email and order

    else:
        messages.error(request, 'Verification Failed')
   
    # return redirect("order-completed")

