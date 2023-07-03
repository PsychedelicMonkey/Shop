from django.conf import settings
from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import stripe


def checkout(request):
    cart = Cart(request)
    return render(request, 'cart/checkout.html', {'cart': cart, 'stripe_client_key': settings.STRIPE_CLIENT_KEY})


def create_payment(request):
    if request.method == 'POST':
        try:
            cart = Cart(request)
            stripe.api_key = settings.STRIPE_SECRET_KEY

            total_price = int(cart.get_total_price() * 100)

            intent = stripe.PaymentIntent.create(
                amount=total_price,
                currency='cad',
            )

            return JsonResponse({
                'clientSecret': intent['client_secret'],
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
    raise Http404


def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'cart/success.html')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd['quantity'], cd['override'])
        return redirect('cart-detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    return redirect('cart-detail')

