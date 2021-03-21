from django import forms
from .models import Reporte, CausaReporte

class ProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=100)

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['causa', 'comentarios']

    causa = forms.ModelChoiceField(
        queryset = CausaReporte.objects.all(),
        widget = forms.RadioSelect
    )