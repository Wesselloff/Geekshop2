from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator

from datetime import datetime


def index(request):
    context = {
        'title': 'geekshop',
        'header': 'GeekShop Store',
        'text': 'Новые образы и лучшие бренды на GeekShop Store. Бесплатная доставка по всему миру! '
                'Аутлет: до -70% Собственный бренд. -20% новым покупателям.'
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'GeekShop - Каталог',
        'year': datetime.now(),
        # 'prods': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }
    if category_id:
        # context.update({'prods': Product.objects.filter(category_id=category_id)})
        products = Product.objects.filter(category_id=category_id)
    else:
        # context.update({'prods': Product.objects.all()})
        products = Product.objects.all()
    paginator = Paginator(products, per_page=3)
    paged_products = paginator.page(page)
    context.update({'prods': paged_products})
    return render(request, 'mainapp/products.html', context)
