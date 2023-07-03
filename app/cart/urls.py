from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart-detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('create-payment/', views.create_payment, name='create-payment'),
    path('success/', views.success, name='success'),
    path('add/<int:product_id>/', views.cart_add, name='cart-add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart-remove'),
]
