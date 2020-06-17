from django.db import models
from django.conf import settings

from products.models import Product

from django.db.models.signals import m2m_changed

User = settings.AUTH_USER_MODEL

# Create your models here.

class CartManager(models.Manager):

	def new_or_get(self, request):
		cart_id = request.session.get("cart_id",None)
		print(cart_id)
		qs = Cart.objects.filter(id=cart_id)
		print(qs.count())
		if qs.count() == 1:
			new_obj = False
			cart_obj = qs.first()
			if request.user.is_authenticated:
				if cart_obj.user is None:
					cart_obj.user = request.user
					cart_obj.save()
		else:
			cart_obj = Cart.objects.new(user=request.user)
			new_obj = True
			request.session["cart_id"] = cart_obj.id
		return cart_obj, new_obj

	def new(self,user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)

class Cart(models.Model):
	user		= models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	products	= models.ManyToManyField(Product, blank=True)
	totalval	= models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
	updated		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)


def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
	if action=='post_add' or action=='post_remove' or action=='post_clear':
		products = instance.products.all()
		total = 0
		for x in products:
			total += x.price
		instance.totalval = total
		instance.save()

m2m_changed.connect(m2m_changed_cart_reciever, sender=Cart.products.through)