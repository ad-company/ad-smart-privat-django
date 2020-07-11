from django import forms
from .models import Base

class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = '__all__'