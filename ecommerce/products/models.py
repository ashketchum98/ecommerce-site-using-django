from django.db import models

# Create your models here.
class Product(models.Model):
	name        = models.CharField(max_length=50)
	description = models.TextField()
	price       = models.DecimalField(max_digits=10, decimal_places=2)
	categories	= (('ER','Electronics'),('CL','Clothes'),('FR','Furniture'))
	category	= models.CharField(max_length=2, choices=categories, null=False)
	img         = models.ImageField(upload_to='product_imgs/', null=True, blank=True)

	def __str__(self):
		return self.name

	def get_url(self):
		if self.category=='ER':
			return '/electronics/' + str(self.id) + '/'
		elif self.category=='CL':
			return '/clothes/' + str(self.id) + "/"
		else:
			return '/furniture/' + str(self.id) + '/'


class LatestDeal(models.Model):
	name        = models.CharField(max_length=50)
	description = models.TextField()
	price       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	img         = models.ImageField(upload_to='latest_deals/', null=True, blank=True)

	def __str__(self):
		return self.name