from django.urls import path

from order.views import *

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('update/', updateCart, name='update'),
    path('add/', addCart, name='add'),
    path('checkout/', checkout, name='checkout'),
    path('process/', processOrder, name='process')
]
