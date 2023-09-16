from django import forms
from .models import ImageModel
class myform(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'