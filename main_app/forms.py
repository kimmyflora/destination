from django import forms
from .models import Hotel, Activity

class ActivityForm(forms.ModelForm):
	class Meta:
		# meta class is configuration options for a class
		# this is straight from the docs
		model = Activity
		fields = ['name', 'city']


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description']
