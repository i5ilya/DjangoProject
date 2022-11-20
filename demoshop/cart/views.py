from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.utils import json

from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add_js(request):
    cart = Cart(request)
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        product_id = jsondata.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        response = JsonResponse({'cart_len': cart.__len__(), 'cart_sum': cart.get_total_price()  })
        return response
    return redirect(request.META['HTTP_REFERER'])