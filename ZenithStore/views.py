# import httpresponse
from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product

# create function
def home(request):
    # fetch product from database
    products = Product.objects.all().filter(is_available=True) # is_available = True means that all the available product will display

    context = {
        'products': products
    }

    # return HttpResponse("Welcome to ZenithStore")
    return render(request,'home.html', context)
