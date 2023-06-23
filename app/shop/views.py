from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from cart.forms import CartAddProductForm
from .models import Product, ProductReview


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_available=True)


class ProductReviewCreate(LoginRequiredMixin, CreateView):
    model = ProductReview
    fields = ('rating', 'title', 'body',)

    def dispatch(self, request, *args, **kwargs):
        # Attach the product pk to the form
        self.product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super(ProductReviewCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.product
        return super().form_valid(form)
