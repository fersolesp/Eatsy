from django import forms
from django.core.validators import FileExtensionValidator
from .models import Receta

class CreateRecipeForm(forms.ModelForm):
    def __init__(self, productos, *args, **kwargs):
        super(CreateRecipeForm, self).__init__(*args, **kwargs)
        self.fields['imagen'] = forms.ImageField(label="Imagen",validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], required=False, widget=forms.FileInput(attrs={'style':'display:None', 'accept':'image/*'}))
        self.fields['nombre'] = forms.CharField(label='Nombre',error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
        self.fields['descripcion'] = forms.CharField(label='Descripción',error_messages={'required':'Este campo no puede estar vacío'}, widget= forms.Textarea(attrs={'class' : 'form-control', 'style':'width : 100%', 'blank':'False'}))
        self.fields['productos']= forms.MultipleChoiceField(label='Selecciona un género', choices=productos, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 100%; height: 15em;'}))
        
   
    class Meta:
        model = Receta
        fields = ('productos', )