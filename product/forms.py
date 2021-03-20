from django import forms

class ProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=100)