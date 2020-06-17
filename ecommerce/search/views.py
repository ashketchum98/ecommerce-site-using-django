from django.shortcuts import render
from products.models import Product
from django.http import HttpResponseRedirect

# Create your views here.

def search(request):
	val = request.GET.get('search', False)
	if val == False:
		return HttpResponseRedirect('/')
	el = Product.objects.filter(name__icontains=val)
	context = { 'qs1': el, 'val': val}
	if el:
		return render(request, 'search.html', context)
	else:
		return render(request, 'search.html', { 'val': 'Not Found' })
