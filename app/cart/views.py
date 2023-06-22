from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


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

