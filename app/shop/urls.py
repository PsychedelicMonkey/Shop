from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<str:slug>/', views.ProductDetail.as_view(), name='product-detail'),
]
