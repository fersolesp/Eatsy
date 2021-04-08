#from django.shortcuts import render
#from django.contrib.auth.decorators import login_required, staff_member_required, user_passes_test #Usar estos métodos para controlar quién puede acceder a las vistas
#Para comprobar si es superuser, poner @user_passes_test(lambda u: u.is_superuser) antes de definir la vista. Con el resto bastaría poner @login_required o @staff_member_required
from authentication.forms import SignUpForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from authentication.models import Perfil, Dieta

def loginPage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect ('/product/list')
            else:
                messages.error(request, 'Nombre de usuario y/o contraseña no es correcto')
                return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form} )