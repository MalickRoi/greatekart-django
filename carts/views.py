from carts.models import Cart, CartItem
from store.models import Product
from django.shortcuts import redirect, render

# Create your views here.
def _cart_id_view(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        #get the cart using the cart_id present in the session
        cart = Cart.objects.get(cart_id=_cart_id_view(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id_view(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart-page')


def cart_view(request):
    return render(request, 'carts/cart.html')

    