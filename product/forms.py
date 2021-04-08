from enum import Enum

from django import forms
from django.core.validators import FileExtensionValidator

from .models import Aportacion, CausaReporte, Producto, Reporte, Ubicacion, User


class CustomMMCF(forms.ModelChoiceField):
    def label_from_instance(self, ubicacion):
        return "%s" % ubicacion.nombre

class CustomMMCF2(forms.ModelMultipleChoiceField):
    def label_from_instance(self, ubicacion):
        return "%s" % ubicacion.nombre

class CreateProductForm(forms.ModelForm):
    foto = forms.ImageField(label="Imagen",validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], required=False, widget=forms.FileInput(attrs={'style':'display:None', 'accept':'image/*'}))
    nombre = forms.CharField(label='Nombre',error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción',error_messages={'required':'Este campo no puede estar vacío'}, widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 100%', 'blank':'False'}))
    precio = forms.DecimalField(label="Precio",max_digits=4, decimal_places=2, min_value=0.01, max_value=99.99, widget=forms.NumberInput(attrs={'class':'form-control'}))
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Gluten', 'Gluten'),
        ('Lactosa', 'Lactosa'),
        ('Marisco', 'Marisco'),
        ('Frutos secos', 'Frutos secos'),
    )

    dieta = forms.MultipleChoiceField(label='Etiqueta', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 350px'}))

    ubicaciones = CustomMMCF(queryset=Ubicacion.objects.all(), required=False, widget=forms.Select(attrs={'class' : 'form-control', 'style':'width : 400px'}))
    class Meta:
        model = Ubicacion
        fields = ['nombre']

    nombreComercio = forms.CharField(label='Nombre del Comercio',strip=True, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput, required=False )
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput ,required=False)

  

class AddUbicationForm(forms.ModelForm):
    ubicaciones = CustomMMCF(queryset= Ubicacion.objects.all().order_by("nombre"),required=False, widget=forms.Select(attrs={'class' : 'form-control'}))
    nombreComercio = forms.CharField(label='Nombre del Comercio', required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    lat =  forms.DecimalField(label='Latitud', widget=forms.HiddenInput, required=False)
    lon = forms.DecimalField(label='Longitud', widget=forms.HiddenInput ,required=False)
    precio = forms.DecimalField(label="Precio",max_digits=4, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Ubicacion
        fields = ['nombreComercio']

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Aportacion
        fields = ['titulo','mensaje']

    titulo= forms.CharField(label='Título', widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

class SearchProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'dietas']
        labels = {
            'titulo': 'Nombre del producto'
        }
        widgets = {
            'dietas': forms.CheckboxSelectMultiple(attrs={"form":"filtros-form", 'class': 'form-check'}),
            'titulo': forms.TextInput(attrs={"class":"w-100 h-100 form-control border border-dark", "placeholder":"Buscar"})
        }

    class OrderBy(Enum):
        newest = ('Más nuevos primero', '-id')
        oldest = ('Más antiguos primero', 'id')
        barato = ('Más baratos primero', 'precioMedio')
        caro = ('Más caros primero', '-precioMedio')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[1]
    
    orderBy = forms.TypedChoiceField(
        choices = [(orderBy.value[1], orderBy.value[0]) for orderBy in OrderBy],
        coerce = OrderBy.get_value,
        required = True,
        initial = OrderBy.newest.name,
        label = 'Ordenar por',
        widget=forms.Select(attrs={"form":"filtros-form", 'class': 'form-control'})
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
    nombre = forms.CharField(label='Nombre',error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    descripcion = forms.CharField(label='Descripción',error_messages={'required':'Este campo no puede estar vacío'}, widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 100%'}))
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
    ubicaciones = CustomMMCF2(queryset= Ubicacion.objects.all(), widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 200px'}))
    
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

class ReviewReporteForm(forms.ModelForm):
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

    Revision_Enum = (("Resuelto", "Resuelto"),
                ("No procede","No procede"))

    revision = forms.ChoiceField(label='Revisar', choices=Revision_Enum, widget = forms.RadioSelect)

class LoginForm(forms.ModelForm):
    username =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))