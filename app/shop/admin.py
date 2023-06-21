from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('img_tag', 'image', 'caption',)
    readonly_fields = ('img_tag',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = (ProductImageInline,)
    prepopulated_fields = {'slug': ['name']}
