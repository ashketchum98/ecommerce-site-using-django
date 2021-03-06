from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from addresses.forms import AddressForm
from addresses.models import Address

# Create your views here.
from .models import Cart
from orders.models import Order
from products.models import Product
from billing.models import BillingProfile
from user.models import GuestEmail

from django.http import JsonResponse
from django.conf import settings

import stripe

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")

STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")


def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{"id": x.id , "url": x.get_url(),"name": x.name, "price": x.price } for x in cart_obj.products.all() ]
	cart_data = {"products": products, "total": cart_obj.totalval }
	return JsonResponse(cart_data)

def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	return render(request, 'carts_home.html', { "cart": cart_obj })

def update(request):
	product_id = request.POST.get('product_id')
	print(product_id)
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("No such product exists")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False
		else:
			cart_obj.products.add(product_obj)
			added = True
		request.session['cart_items'] = cart_obj.products.count()

		if request.is_ajax():
			json_data = {
				"added": added,
				"removed": not added,
				"cartItemCount": cart_obj.products.count(),

			}
			return JsonResponse(json_data)
	return redirect('cart:home')

def checkout_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	order_obj = None
	if new_obj or cart_obj.products.count() == 0:
		return redirect("cart:home") 

	address_form = AddressForm() 
	billing_address_id = request.session.get("billing_address_id",None)
	shipping_address_id = request.session.get("shipping_address_id",None)

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	has_card = False

	address_qs = None
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id = shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id = billing_address_id)
			del request.session["billing_address_id"]
		if shipping_address_id or billing_address_id:
			order_obj.save()
		has_card = billing_profile.has_card

	if request.method=="POST":
		is_prepared = order_obj.check_done()
		if is_prepared:
			did_charge, crg_msg = billing_profile.charge(order_obj)
			if did_charge:
				order_obj.mark_paid()
				request.session['cart_items'] = 0
				del request.session['cart_id']
				if not billing_profile.user:
					billing_profile.set_cards_inactive()
				return redirect("cart:success")
			else:
				print(crg_msg)
				return redirect("cart:checkout")

	context = {
	"object" : order_obj,
	"billing_profile": billing_profile,
	"address_form": address_form,
	"address_qs": address_qs,
	"has_card": has_card,
	"publish_key": STRIPE_PUB_KEY,
	}
	return render(request, "checkout.html", context)


def checkout_done_view(request):
	return render(request, "checkout_done.html")

