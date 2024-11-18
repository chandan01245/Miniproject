from django import forms
from django.forms import ModelForm

from .models import medicine, register


class register_form(ModelForm):
    class Meta:
        model = register
        fields = '__all__'
        
class medication_form(ModelForm):
    class Meta:
        model = medicine
        fields = '__all__'
