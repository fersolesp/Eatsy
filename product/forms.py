from django import forms
from .models import Reporte, CausaReporte, Producto, Ubicacion

from enum import Enum

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, ubicacion):
        return "%s" % ubicacion.nombre


class CreateProductForm(forms.ModelForm):
    foto= forms.ImageField(label="Imagen", required= False, widget=forms.FileInput(attrs={'hidden': 'True'}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción', widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 100%'}))
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
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput, required=False)
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput ,required=False)

    class Meta:
        model = Ubicacion
        fields = ['nombre']

class AddUbicationForm(forms.ModelForm):
    ubicaciones = CustomMMCF(queryset= Ubicacion.objects.all(),required=False, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 400px'}))
    nombreComercio = forms.CharField(label='Nombre del Comercio', required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput, required=False)
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput ,required=False)
    precio = forms.DecimalField(label="Precio",max_digits=4, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ubicacion
        fields = ['nombre']

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['causa', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'class': 'form-control'})
        }
    
    causa = forms.ModelChoiceField(
        queryset = CausaReporte.objects.all(),
        widget = forms.RadioSelect
    )

class SearchProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'dietas']
        labels = {
            'titulo': 'Nombre del producto'
        }
        widgets = {
            'dietas': forms.CheckboxSelectMultiple()
        }

    class OrderBy(Enum):
        newest = ('Más nuevos primero', '-id')
        oldest = ('Más antiguos primero', 'id')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[1]
    
    orderBy = forms.TypedChoiceField(
        choices = [(orderBy.name, orderBy.value[0]) for orderBy in OrderBy],
        coerce = OrderBy.get_value,
        required = True,
        initial = OrderBy.newest.name,
        label = 'Ordenar por'
    )

    def __init__(self, *args, **kwargs):
        super(SearchProductForm, self).__init__(*args, **kwargs)
        
        self.fields['titulo'].required = False
        self.fields['dietas'].required = False
        
        # Rellenar para el segundo sprint con las dietas del usuario
        # self.fields['dietas'].initial = [  ]

class MiniSearchProductForm(SearchProductForm):
    def __init__(self, *args, **kwargs):
        super(MiniSearchProductForm, self).__init__(*args, **kwargs)
        
        self.fields['dietas'].widget = forms.MultipleHiddenInput()
        self.fields['orderBy'].widget = forms.HiddenInput()

class ReviewProductForm(forms.ModelForm):
    foto= forms.ImageField(label="Imagen", required= False, widget=forms.FileInput(attrs={'hidden': 'True'}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción', widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 100%'}))
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
    
    Revision_Enum = (
        ('Aceptar', 'Aceptar'),
        ('Denegar', 'Denegar'),
    )
    revision = forms.ChoiceField(label='Revisar', choices=Revision_Enum, widget = forms.RadioSelect)

    nombreComercio = forms.CharField(label='Nombre del Comercio', required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput, required=False)
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput, required=False)

    class Meta:
        model = Ubicacion
        fields = ['nombre']

class AddDietForm(forms.ModelForm):
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Gluten', 'Gluten'),
        ('Lactosa', 'Lactosa'),
        ('Marisco', 'Marisco'),
        ('Frutos secos', 'Frutos secos'),
    )
    dieta = forms.MultipleChoiceField(label='Etiqueta', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 350px'}))
    class Meta:
        model = Ubicacion
        fields = ['nombre']