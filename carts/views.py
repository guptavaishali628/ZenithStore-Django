from django.shortcuts import render

# Create your views here.
# cart function
def cart(request):
    return render(request, 'carts/cart.html')
