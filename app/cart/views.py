from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
import stripe


@require_POST
def checkout(request):
    try:
        cart = Cart(request)
        line_items = []
        for item in cart:
            line_items.append({
                'price_data': {
                    'currency': 'cad',
                    'product_data': {
                        'name': item['product'].name,
                    },
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            })

        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success.html',
            cancel_url='http://localhost:8000/cart/'
        )
        return redirect(checkout_session.url)
    except Exception as e:
        print(str(e))


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

