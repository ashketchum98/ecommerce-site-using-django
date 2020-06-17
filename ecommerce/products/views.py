from django.shortcuts import render
from .models import Product

from carts.models import Cart

from analytics.signals import object_viewed_signal

# Create your views here.

def pro(request,value):
	qs = Product.objects.filter(category=value)
	cart = Cart.objects.new_or_get(request)
	return render(request, 'products.html', { 'qs': qs, 'cart': cart[0] })

def pro_details(request, **kwargs):
	pro_id = kwargs['pk']
	qs = Product.objects.filter(pk=pro_id)
	cart = Cart.objects.new_or_get(request)
	if qs.first() is None:
		return render(request, 'details.html', {'empty': 'No Such Product'})
	if request.user.is_authenticated:
		object_viewed_signal.send(qs.first().__class__, instance=qs.first(), request=request)
	return render(request, 'details.html', { 'qs': qs, 'cart': cart[0] })

