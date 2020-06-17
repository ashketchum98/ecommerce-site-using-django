from django.db import models

class ContactInfo(models.Model):
	fname = models.CharField(max_length=20)
	city = models.CharField(max_length=20)
	subject = models.CharField(max_length=500)

	def __str__(self):
		return self.fname

class GuestEmail(models.Model):
	email = models.EmailField()
	active		= models.BooleanField(default=True)
	update		= models.DateTimeField(auto_now=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.email

class Profile(models.Model):
	username  = models.CharField(max_length=20)
	full_name = models.CharField(max_length=20)
	dob 	  = models.DateField()
	address   = models.TextField()
	mobile_no = models.IntegerField()

	def __str__(self):
		return self.full_name