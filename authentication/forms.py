from django import forms
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
    username =  forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario', max_length=150, validators=[ASCIIUsernameValidator], error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    nombre = forms.CharField(label='Nombre', max_length=150, error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    apellidos = forms.CharField(label='Apellidos', max_length=150, error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    email =  forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Sin gluten', 'Sin gluten'),
        ('Sin lactosa', 'Sin lactosa'),
        ('Sin marisco', 'Sin marisco'),
        ('Sin frutos secos', 'Sin frutos secos'),
    )
    dieta = forms.MultipleChoiceField(label='Dieta o intolerancias', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control'}))
    password_validator = RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', 'La contraseña debe contener entre 8 y 64 caracteres, tener una letra mayúscula, una minúscula, un dígito y un carácter especial')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class' : 'form-control'}), validators=[password_validator], strip=False)
    v_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class' : 'form-control'}), validators=[password_validator], strip=False)
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

class resetPasswordForm(forms.Form):
    password_validator = RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', 'La contraseña debe contener entre 8 y 64 caracteres, tener una letra mayúscula, una minúscula, un dígito y un carácter especial')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class' : 'form-control'}), validators=[password_validator], strip=False)
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'class' : 'form-control'}), validators=[password_validator], strip=False)
    v_new_password = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput(attrs={'class' : 'form-control'}), validators=[password_validator], strip=False)
    
    def clean(self):
        clean_data = super(resetPasswordForm, self).clean()
        new_password = clean_data.get('new_password')
        v_new_password = clean_data.get('v_new_password')
        if new_password != v_new_password:
            self.add_error('v_new_password', 'La nueva contraseña y su confirmación no coinciden')
        return clean_data

class ProfileForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=150, error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    apellidos = forms.CharField(label='Apellidos', max_length=150, error_messages={'required':'Este campo no puede estar vacío'}, widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    Dieta_Enum = (
        ('Vegano', 'Vegano'),
        ('Vegetariano', 'Vegetariano'),
        ('Sin gluten', 'Sin gluten'),
        ('Sin lactosa', 'Sin lactosa'),
        ('Sin marisco', 'Sin marisco'),
        ('Sin frutos secos', 'Sin frutos secos'),
    )
    dieta = forms.MultipleChoiceField(label='Dieta o intolerancias', choices=Dieta_Enum, widget=forms.SelectMultiple(attrs={'class' : 'form-control'}))
    activada = forms.BooleanField(label='Cuenta ya activada', disabled=True, required=False)

