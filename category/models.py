from django.db import models

from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='category', null=True)

    def get_absolute_url(self):
        return reverse('category/', args=[self.slug])

    def __str__(self):
        return self.title
