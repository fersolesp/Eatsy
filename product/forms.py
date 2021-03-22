from django import forms
from .models import Reporte, CausaReporte, Producto, Ubicacion

class ProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=100)


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, ubicacion):
        return "%s" % ubicacion.nombre


class CreateProductForm(forms.ModelForm):
    foto= forms.ImageField(label="Imagen", required= False, widget=forms.FileInput(attrs={'hidden': 'True'}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción', widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 300%'}))
    precio = forms.DecimalField(label="Precio",max_digits=4, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class':'form-control'}))
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Gluten', 'Gluten'),
        ('Lactosa', 'Lactosa'),
        ('Marisco', 'Marisco'),
        ('Frutos secos', 'Frutos secos'),
    )
    dieta = forms.MultipleChoiceField(label='Etiqueta', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 350px'}))

    ubicaciones = CustomMMCF(queryset= Ubicacion.objects.all(),required=False, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 400px'}))


    nombreComercio = forms.CharField(label='Nombre del Comercio', required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput, required=False )
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput ,required=False)

    class Meta:
        model = Ubicacion
        fields = ['nombre']

    

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['causa', 'comentarios']

    causa = forms.ModelChoiceField(
        queryset = CausaReporte.objects.all(),
        widget = forms.RadioSelect
    )
