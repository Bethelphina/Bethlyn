from django.shortcuts import render
from store.models import Product
from category.models import Category
# from ads.models import MainAds


def index(request):
    featured_products = Product.objects.filter(is_featured=True)
    various_category = Category.objects.all()
    # main_ads = MainAds.objects.all()
    context = {
        'featured_products':featured_products,
        'various_category':various_category,
        # 'main_ads':main_ads
    }
    return render(request, 'index.html', context)