from django import forms
from .models import Producto, Ubicacion
class ProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=100)


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, ubicacion):
        return "%s" % ubicacion.nombre


class CreateProductForm(forms.ModelForm):
    foto= forms.ImageField(label="Imagen", required= False)
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción', widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 800px'}))
    precio = forms.DecimalField(label="Precio",max_digits=4, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class':'form-control'}))
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Gluten', 'Gluten'),
        ('Lactosa', 'Lactosa'),
        ('Marisco', 'Marisco'),
        ('Frutos secos', 'Frutos secos'),
    )
    dieta = forms.MultipleChoiceField(label='Etiqueta', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 200px'}))

    ubicaciones = CustomMMCF(queryset= Ubicacion.objects.all(), widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 200px'}))

    class Meta:
        model = Ubicacion
        fields = ['nombre']

class CreateNewUbication(forms.Form):
    nombreComercio = forms.CharField(label='Nombre del Comercio', widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput )
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput )

