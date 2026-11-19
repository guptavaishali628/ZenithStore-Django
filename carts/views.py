from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product, Variation
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
    product_variation = []
    # take the value from brows url because we are using get request(for product variation)
    if request.method == 'POST':
    #    color = request.POST.get('color') # color= name of selected value from dropdown
    #    size = request.POST.get('size')
    #    print(color, size)
    #    here will will make our code to handle all the situations instead of only dealing with color and size
        for item in request.POST:
            key = item
            value = request.POST[key]
            # key and value should match from the variation model values

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass    

    try:
        #get the cart using the cart_id present in the session
        cart=Cart.objects.get(cart_id=cart_id(request)) 
    
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=cart_id(request)
        )
    cart.save()
    
    # here we will put the product inside the cart then the product becomes a cart item , in one cart there are multiple products , so will do to combine this product and cart to get the cart item
    
    # first check cart item is available or not
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    # try:
    if is_cart_item_exists:
        # cart_item = CartItem.objects.get(product=product, cart=cart)

        # for grouping cart item variation
        # cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

        # instead of creating we have to filter the cart item
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        # existing variations--> database
        # current variation--> product variations
        # item_id--> coming from database
        # if the current variation inside the existing variation then we are going to increase the quantity
        ex_var_list = []
        # cart_item_id
        id=[]
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(set(existing_variation))
            id.append(item.id)
        print(ex_var_list) 

        if set(product_variation) in ex_var_list:
            # increase the cart item quantity
            index = ex_var_list.index(set(product_variation))
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity+=1
            item.save()

        else:  
            # Add Variation in Cart Item
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation)>0:
                item.variations.clear()
                item.variations.add(*product_variation)
            # as we have added the quantity in create () then we dont need here
            # cart_item.quantity += 1
            item.save()

    # except CartItem.DoesNotExist: 
    else:
        # so will create a new cart item
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )    
        # Add Variation in Cart Item
        if len(product_variation)>0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')    
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
# here we will pass the cart_item_id as well as on url
def remove_cart_item(request, product_id, cart_item_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    cart_item=CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
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
