import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from store.models import Product
from category.models import Category
from .models import Order, OrderItem, ShippingAdress


def cart(request):
    category_list = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
        products = Product.objects.filter(likes__username=request.user.username)
        likes = products.count()
        totalPrice = order.get_total_price

    else:
        items = []
        cartItems = 0
        likes = 0
        totalPrice = 0
    context = {
        'items': items,
        'cartItems': cartItems,
        'likes': likes,
        'totalPrice': totalPrice,
        'category_list': category_list
    }
    return render(request, 'order/cart.html', context)


@csrf_exempt
def addCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    order, created = Order.objects.get_or_create(customer=request.user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product_id=productId)
    orderItem.quantity = (orderItem.quantity + int(data['quantity']))
    orderItem.save()
    return JsonResponse("Success", safe=False)


@csrf_exempt
def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    order, created = Order.objects.get_or_create(customer=request.user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product_id=productId)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.quantity = (orderItem.quantity + int(data['quantity']))
    orderItem.save()

    if orderItem.quantity < 1 or action == 'delete':
        orderItem.delete()

    return JsonResponse("Success", safe=False)


@login_required
def checkout(request):
    category_list = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
        products = Product.objects.filter(likes__username=request.user.username)
        likes = products.count()
        totalPrice = order.get_total_price
    else:
        items = []
        cartItems = 0
        likes = 0
        totalPrice = 0
    context = {
        'items': items,
        'cartItems': cartItems,
        'likes': likes,
        'totalPrice': totalPrice,
        'category_list': category_list
    }
    return render(request, 'order/checkout.html', context)


def processOrder(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        order.save()
        ShippingAdress.objects.create(
            order=order,
            customer=customer,
            phone=data['shippingInfo']['phone'],
            address1=data['shippingInfo']['address1'],
            address2=data['shippingInfo']['address2'],
            country=data['shippingInfo']['country'],
            city=data['shippingInfo']['city'],
            state=data['shippingInfo']['state'],
            zip_code=data['shippingInfo']['zipCode']
        )
    return JsonResponse("Success", safe=False)
