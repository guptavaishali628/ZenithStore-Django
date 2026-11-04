from django.shortcuts import redirect, render
from store.models import Product
from .  models import Cart, CartItem

# Create your views here.
# Add_cart function
def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    # get the product
    product = Product.objects.get(id=product_id)
    try:
        #get the cart using the cart_id present in the session
        cart=Cart.objects.get(cart_id=cart_id(request)) 
    
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=cart_id(request)
        )
    cart.save()
    
    # here we will put the product inside the cart then the product becomes a cart item , in one cart there are multiple products , so will do to combine this product and cart to get the cart item
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist: 
        # so will create a new cart item
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )    
        cart_item.save()

    # redirect to cart
    return redirect('cart')

# cart function
def cart(request):
    return render(request, 'carts/cart.html')
