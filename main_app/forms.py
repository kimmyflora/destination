from django.forms import ModelForm
from .models import Activity

class ActivityForm(ModelForm):
	class Meta:
		# meta class is configuration options for a class
		# this is straight from the docs
		model = Activity
		fields = ['name', 'city']