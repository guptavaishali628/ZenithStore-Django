from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from .  models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

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
    # print cart_item and product name
    # return HttpResponse(cart_item.product) # name of the cart item product
    # return HttpResponse(cart_item.quantity)  # print the quantity of the cart item product

    # exit()

    # redirect to cart
    return redirect('cart')

# remove cart function
def remove_cart(request, product_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    cart_item=CartItem.objects.get(product=product, cart=cart)
    # condition
    if cart_item.quantity > 1:
        # decreament the quantity of the cart item by 1
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()    
    return redirect('cart')

# remove cart item function
def remove_cart_item(request, product_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    cart_item=CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

# cart function
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        # calculating tax and total
        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass # just ignore     

    context={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        # tax and grand_total
        'tax': tax,
        'grand_total': grand_total,
    }   
    return render(request, 'carts/cart.html',context)
