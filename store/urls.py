from django.urls import path 
from .views import store,productdetail, search, submit_review


urlpatterns = [
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='product_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', productdetail, name='product_detail'),
    path('search/', search, name='search'),

    path('submit_review/<int:product_id>', submit_review, name='submit_review'),
]
 