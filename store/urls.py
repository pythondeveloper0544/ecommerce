from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('category/<slug:slug>/', ProductsByCategoryView.as_view(), name='category'),
    path('detail/<slug:slug>', ProductDetailView.as_view(), name='detail'),
    path('search/', search_view, name='search'),
    path('product/create/', ProductCreateView.as_view(), name='create-product'),
    path('product/update/<slug:slug>', ProductUpdateView.as_view(), name='update-product'),
    path('liked/', likedProduct, name='liked')
]
