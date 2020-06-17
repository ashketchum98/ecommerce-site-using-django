from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
# Create your views here.
from .forms import AddressForm
from billing.models import BillingProfile
from .models import Address


def checkout_address_create_view(request):
	form = AddressForm(request.POST or None)
	context = {
		'form': form
	}
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirected_path = next_ or next_post or None
	if form.is_valid():
		print(request.POST)
		instance = form.save(commit=False)

		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		
		if billing_profile is not None:
			address_type = request.POST.get('address_type','shipping')
			instance.billing_profile = billing_profile
			instance.address_types = address_type
			instance.save()

			request.session[address_type + '_address_id'] = instance.id 
			billing_address_id = request.session.get("billing_address_id",None)
			shipping_address_id = request.session.get("shipping_address_id",None)

		else:
			print("Error")
			return redirect("cart:checkout")
		if is_safe_url(redirected_path, request.get_host()):
			return redirect(redirected_path)
	return redirect('cart:checkout')


def checkout_address_reuse_view(request):
	if request.user.is_authenticated:
		context = {}
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirected_path = next_ or next_post or None

		if request.method == "POST":
			print(request.POST)
			shipping_address = request.POST.get("shipping_address", None)
			address_type = request.POST.get('address_type','shipping')
			billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
			if shipping_address is not None:
				qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
				if qs.exists():
					request.session[address_type + '_address_id'] = shipping_address
				if is_safe_url(redirected_path, request.get_host()):
					return redirect(redirected_path)
	return redirect('cart:checkout')