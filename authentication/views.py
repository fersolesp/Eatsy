#from django.shortcuts import render
from django.contrib.auth.decorators import login_required #, staff_member_required, user_passes_test #Usar estos métodos para controlar quién puede acceder a las vistas
#Para comprobar si es superuser, poner @user_passes_test(lambda u: u.is_superuser) antes de definir la vista. Con el resto bastaría poner @login_required o @staff_member_required
from authentication.forms import SignUpForm, LoginForm, ProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from authentication.models import Perfil, Dieta

def loginPage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # if user.is_active:
                login(request, user)
                return redirect('/product/list')
                # else:
                #     form.add_error('password', 'Inicio de sesión incorrecto')
                #     return render(request, 'login.html', {'form':form})
            else:
                form.add_error('password', 'Inicio de sesión incorrecto')
                return render(request, 'login.html', {'form':form})    
    return render(request, 'login.html', {'form':form})

def signUp(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Comprobar que no haya usuario con el mismo correo
            if User.objects.filter(email=form.cleaned_data['email']).count() > 0:
                form.add_error('email', 'El email indicado ya está en uso')
                return render(request, 'signUp.html', {'form': form})
            # Comprobar que no haya usuario con mismo username
            if User.objects.filter(username=form.cleaned_data['username']).count() > 0:
                form.add_error('username', 'El nombre de usuario indicado ya está en uso')
                return render(request, 'signUp.html', {'form': form})
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellidos']
            user.save()
            perfil = Perfil(user=user)
            perfil.save()
            for dieta in form.cleaned_data['dieta']:
                perfil.dietas.add(get_object_or_404(Dieta, nombre=dieta))
            return redirect('/authentication/login')
    return render(request, 'signUp.html', {'form': form})

@login_required(login_url='/authentication/login')
def logout_view(request):
    logout(request)
    return redirect("/")

def subscribe(request):
 
    return render(request, 'subscribe.html')

@login_required(login_url='/authentication/login')
def myProfile(request):
    user = request.user
    perfil = get_object_or_404(Perfil, user=user)
    
    if request.method == 'POST':
        
        form = ProfileForm(request.POST)
        print(form.errors)
        if form.is_valid():
            
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellidos']
            user.save()
            perfil.dietas.clear()
            for dieta in form.cleaned_data['dieta']:
                perfil.dietas.add(get_object_or_404(Dieta, nombre=dieta))
            perfil.save()
    data = {
            'nombre': user.first_name,
            'apellidos': user.last_name,
            'dieta': [dieta.nombre for dieta in perfil.dietas.all()],
            'activada': perfil.activeAccount
        }
    form = ProfileForm(initial=data)
    return render(request, 'perfil.html', {'form': form})


