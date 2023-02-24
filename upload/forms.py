from django import forms
from upload.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['prod_name']
