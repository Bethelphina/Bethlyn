from django.urls import path 
# from .views import store,productdetail, search, submit_review
from .views import VendorListView, vendordetail

urlpatterns = [
    path('', VendorListView.as_view(), name='vendorslist'),
    # path('category/<slug:category_slug>/', store, name='product_category'),
    path('<slug:vendor_slug>', vendordetail, name='vendor_detail'),
    # path('search/', search, name='search'),

    # path('submit_review/<slug:product_slug>', submit_review, name='submit_review'),
]
 