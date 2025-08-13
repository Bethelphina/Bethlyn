from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Vendor
# Create your views here.

class VendorListView(ListView):
    queryset = Vendor.objects.all()
    template_name = 'vendors/vendorlist.html'


def vendordetail(request, vendor_slug):
    single_vendor = Vendor.objects.get(slug = vendor_slug)
    context = {
        "singlevendor":single_vendor,
    }
    return render(request, 'vendors/singlevendordetail.html', context)