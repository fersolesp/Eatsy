from django import forms
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
    username =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario', max_length=150, validators=[ASCIIUsernameValidator], error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) ) 
    nombre = forms.CharField(label='Nombre', max_length=150, error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    apellidos = forms.CharField(label='Apellidos', max_length=150, error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    email =  forms.EmailField(label='Email')
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Gluten', 'Gluten'),
        ('Lactosa', 'Lactosa'),
        ('Marisco', 'Marisco'),
        ('Frutos secos', 'Frutos secos'),
    )
    dieta = forms.MultipleChoiceField(label='Dieta', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control', 'style':'width : 350px'}))
    password_validator = RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', 'La contraseña debe contener entre 8 y 64 caractetes, tener una letra mayúscula, una minúscula, un dígito y un carácter especial')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, validators=[password_validator])
    v_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, validators=[password_validator])
    
    def clean(self):
        clean_data = super(SignUpForm, self).clean()
        password = clean_data.get('password')
        v_password = clean_data.get('v_password')
        if password != v_password:
            self.add_error('v_password', 'La contraseña y su confirmación no coinciden')
        return clean_data
    
    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellidos']
