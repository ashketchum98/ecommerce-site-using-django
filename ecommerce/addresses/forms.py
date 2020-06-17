from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields=[
			#'billing_profile',
			#'address_types',
			'address_line_1',
			'address_line_2',
			'city',
			'state',
			'country',
			'postal_code',
		]
