from django import forms
from .models import ImageModel
class myform(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Image'].label = ''