from django import forms
from .models import Tentors

class TentorForm(forms.ModelForm):
    class Meta:
        model = Tentors
        fields = '__all__'