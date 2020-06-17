from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect , HttpResponse
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import ContactInfo, Profile, GuestEmail
from products.models import LatestDeal, Product
from datetime import datetime
from django.utils.http import is_safe_url

from .signals import user_logged_in

# Create your views here.
def home(request):
	deals = LatestDeal.objects.all()
	items = Product.objects.all()
	context = { 'deals' : deals, 'items': items }
	return render(request,'home.html', context)

def about(request):
	return render(request,'about.html')

def contact(request):
	if request.method == "POST":
		info = ContactInfo()
		info.fname = request.POST['fullname']
		info.city = request.POST['city']
		info.subject = request.POST['subject']
		info.save()
		messages.add_message(request, messages.INFO, 'Your Info is recorded we will contact you back ASAP')
		return HttpResponseRedirect('/contact/')
	return render(request,'contact.html')

def profile(request):
	qs = Profile.objects.filter(username=request.user.username)
	if qs:
		context = {
			'fullname': qs[0].full_name,
			'dob'     : qs[0].dob,
			'address' : qs[0].address,
			'mobile'  : qs[0].mobile_no,
		}
		return render(request,'profile.html', context)
	return render(request,'profile.html')

def update(request):
	if request.method == "POST":
		profile_info = Profile()
		profile_info.username  = request.user.username
		profile_info.full_name = request.POST['fullname']
		profile_info.dob       = request.POST['dob']
		profile_info.address   = request.POST['address']
		profile_info.mobile_no = request.POST['number']

		qs = Profile.objects.filter(username=profile_info.username)
		if qs:
			qs[0].full_name = profile_info.full_name
			qs[0].dob       = profile_info.dob
			qs[0].address   = profile_info.address
			qs[0].mobile_no = profile_info.mobile_no
			qs[0].save()
		else:
			profile_info.save()
		messages.add_message(request, messages.INFO, 'Profile Updated !')
		return render(request,'updateprofile.html')
	data = Profile.objects.filter(username=request.user.username)
	if data:
		context = {
			'fullname' : data[0].full_name,
			'dob'      : data[0].dob,
			'address'  : data[0].address,
			'mobile'   : data[0].mobile_no,
		}
		return render(request,'updateprofile.html', context)
	return render(request,'updateprofile.html')


def guest_register_view(request):
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirected_path = next_ or next_post or None
	if request.method == "POST":
		email = request.POST['email']
		new_guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = new_guest_email.id
		if is_safe_url(redirected_path, request.get_host()):
			return HttpResponseRedirect(redirected_path)
		else:
			return HttpResponseRedirect('/register/')
	return HttpResponseRedirect('/register/')


def login_page(request):
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirected_path = next_ or next_post or None
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		if User.objects.filter(username=username).exists():
			user = authenticate(username=username, password= password)
			if user:
				login(request, user)
				user_logged_in.send(user.__class__, instance=user, request=request)
				try:
					del request.session['guest_email_id']
				except:
					pass
				if is_safe_url(redirected_path, request.get_host()):
					return HttpResponseRedirect(redirected_path)
				else:
					return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.INFO, 'Incorrect Username or Password')
				return render(request,'login.html')
		else:
			messages.add_message(request, messages.INFO, 'Incorrect Username or Password')
			return render(request,'login.html')

	return render(request,'login.html')

def signup_page(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
			User.objects.create_user(username, email, password)
			user = authenticate(username = username, password = password)
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			messages.add_message(request, messages.INFO, 'Username or Email already exists !')
			return render(request,'signup.html')
	return render(request,'signup.html')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")