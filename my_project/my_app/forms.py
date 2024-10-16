from django import forms
from .models import Tower

class Towerform(forms.ModelForm):
    class Meta:
        model = Tower
        fields = ['name', 'location', 'file']  
