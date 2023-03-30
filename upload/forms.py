from django import forms
from upload.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['prod_name']

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=100)
    file = forms.FileField()
