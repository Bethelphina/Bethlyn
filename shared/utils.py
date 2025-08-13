import random
import string

from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    new_order_id = random_string_generator().upper()
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_order_id



def unique_id_generator(instance):
    new_id = random_string_generator().upper()
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(cart_id=new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        # slug = slugify(instance.title)
        slug = slugify(random_string_generator(size=6, chars=string.ascii_lowercase))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        randstr = random_string_generator(size=4)
        slug=slug
        new_slug= f'{slug}-{randstr}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_order_generator(instance, order_number=None):
    if order_number is not None:
        order_number = order_number
    else:
        order_number = slugify(random_string_generator(size=8, chars=string.ascii_lowercase + string.digits))

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_number=order_number).exists()
    if qs_exists:
        randstr = random_string_generator(size=4)
        order_number=order_number
        order_number= f'{order_number}-{randstr}'
        return unique_order_generator(instance, order_number=order_number)
    return order_number

