from enum import Enum

from django import forms
from django.core.validators import FileExtensionValidator

from .models import Receta
from product.models import Producto


class CreateRecipeForm(forms.ModelForm):
    imagen = forms.ImageField(label="Imagen",validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], required=False, widget=forms.FileInput(attrs={'style':'display:None', 'accept':'image/*'}))
    nombre = forms.CharField(label='Nombre',error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción',error_messages={'required':'Este campo no puede estar vacío'}, widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 100%', 'blank':'False'}))
    
    productos = Producto.objects.all()

    Producto_Enum = tuple(map(lambda producto: (producto.titulo, producto.titulo), productos))

    productos = forms.MultipleChoiceField(label='Etiqueta', choices=Producto_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 100%; height:15em'}))
    class Meta:
        model = Receta
        fields = ['nombre']