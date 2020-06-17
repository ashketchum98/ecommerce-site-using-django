from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
# Create your views here.
from .models import BillingProfile, Card
from django.conf import settings

import stripe

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")

STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")


def payment_method_view(request):
	billing_profile, created = BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		redirect("/cart")
	next_url = None
	next_ = request.GET.get('next')
	if is_safe_url(next_, request.get_host()):
		next_url = next_
		print(next_url)
	return render(request, "payment_method.html", {"publish_key": STRIPE_PUB_KEY, 'next_url': next_url })


def payment_method_createview(request):
	if request.method == "POST" and request.is_ajax():
		billing_profile, created = BillingProfile.objects.new_or_get(request)
		if not billing_profile:
			return HttpResponse({'message': 'Cannot Find this User'}, status_code=401)
		token = request.POST.get('token')
		if token is not None:
			new_card_obj = Card.objects.add_new(billing_profile, token)
			return JsonResponse({'message': 'Success! Your Card is added'})
	return HttpResponse('Error', status_code=401)