from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from category.models import Category


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('product-detail/', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    @property
    def get_total_likes(self):
        total = self.likes.count()
        return total
