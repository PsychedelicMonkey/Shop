from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Product


def home(request):
    products = Product.objects.filter(is_available=True)

    return render(request, 'shop/home.html', {'products': products})


class ProductList(ListView):
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_available=True)


class ProductDetail(DetailView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_available=True)
