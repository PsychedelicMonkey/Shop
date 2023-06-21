from django.db import models
from django.utils.safestring import mark_safe


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=300, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, null=False, blank=False)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product", null=False, blank=False)
    caption = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def url(self):
        try:
            return self.image.url
        except ValueError:
            return None

    def img_tag(self):
        return mark_safe(f'<img src="{self.url}" alt="" width="100" />')
