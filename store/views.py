from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from carts.models import CartItem
from carts.views import cart_id
# Create your views here.

# store function
def store(request, category_slug=None):
       
        categories = None
        products = None

        if category_slug != None:
           categories = get_object_or_404(Category, slug=category_slug)
           products = Product.objects.all().filter(category=categories, is_available=True)
           product_count = products.count()     

        else:   
           products = Product.objects.all().filter(is_available=True)
           # product count
           product_count = products.count()
        context={
                'categories':categories,
                'products':products,
                'product_count':product_count,

        }
        return render(request,'store/store.html', context)

# product detail function

def product_detail(request, category_slug, product_slug):
        # single product view
        try:
           single_product = get_object_or_404(Product,category__slug=category_slug, slug=product_slug)
         # for checking if the product is already in the cart
           in_cart = CartItem.objects.filter(cart__cart_id= cart_id(request), product=single_product).exists()
        except Exception as e:
            raise e
        context={ 
             'single_product': single_product,
             # pass the in_cart variable to the template
               'in_cart': in_cart,
        }
        return render(request,'store/product_detail.html', context)

