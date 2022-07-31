from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from order.models import Order
from .models import Category
from store.models import Product


def categoryList(request):
    category_list = Category.objects.all()

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        cartItems = order.get_total_items
        products = Product.objects.filter(likes__username=request.user.username)
        likes = products.count()
    else:
        cartItems = 0

    return render(request, 'inc/_nav.html', {'category_list': category_list, 'cartItems': cartItems, 'likes': likes})
