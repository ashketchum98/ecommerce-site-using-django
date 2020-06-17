from django.contrib import admin
from .models import ContactInfo, Profile, GuestEmail

# Register your models here.

admin.site.register(ContactInfo);
admin.site.register(Profile);
admin.site.register(GuestEmail);