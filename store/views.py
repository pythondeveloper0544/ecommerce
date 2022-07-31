import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from order.models import Order
from .forms import ProductForm
from .models import Product
from category.models import Category
from django.views.decorators.csrf import csrf_exempt


class ProductListView(ListView):
    model = Product
    template_name = "store/index.html"
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(product__is_available=True).annotate(Count('product'))
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user, complete=False)
            context['cartItems'] = order.get_total_items
            products = Product.objects.filter(likes__username=self.request.user.username)
            context['likes'] = products.count()
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(is_available=True)[:8]


class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'store/shop.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user, complete=False)
            context['cartItems'] = order.get_total_items
            products = Product.objects.filter(likes__username=self.request.user.username)
            context['likes'] = products.count()
        return context

    def get_queryset(self):
        qs = Product.objects.filter(category__slug=self.kwargs['slug'])
        return qs


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user, complete=False)
            context['cartItems'] = order.get_total_items
            products = Product.objects.filter(likes__username=self.request.user.username)
            context['likes'] = products.count()
        return context


@csrf_exempt
def search_view(request):
    if request.POST:
        search = request.POST['query']
        products = Product.objects.filter(product_name__contains=search)
        category_list = Category.objects.all()
        return render(request, 'store/shop.html', {'products': products, 'category_list': category_list})
    else:
        return render(request, 'store/shop.html', {})


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = 'superuser/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.slug = slugify(product.product_name)
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'superuser/update.html'
    success_url = reverse_lazy('home')


@csrf_exempt
def likedProduct(request):
    data = json.loads(request.body)
    productId = data['productId']
    product = Product.objects.get(id=productId)
    if not product.likes.exists():
        product.likes.add(request.user)
    else:
        product.likes.remove(request.user)
    return JsonResponse(data)
