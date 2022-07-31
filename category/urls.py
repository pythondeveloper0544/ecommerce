from django.urls import path

from category.views import categoryList

urlpatterns = [
    path('categories/', categoryList, name='category_list')
]
