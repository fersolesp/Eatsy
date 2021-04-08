#from django.shortcuts import render
#from django.contrib.auth.decorators import login_required, staff_member_required, user_passes_test #Usar estos métodos para controlar quién puede acceder a las vistas
#Para comprobar si es superuser, poner @user_passes_test(lambda u: u.is_superuser) antes de definir la vista. Con el resto bastaría poner @login_required o @staff_member_required
from authentication.forms import SignUpForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from authentication.models import Perfil, Dieta

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
            user.name = form.cleaned_data['nombre']
            user.lastname = form.cleaned_data['apellidos']
            user.save()
            perfil = Perfil(user=user)
            perfil.save()
            for dieta in form.cleaned_data['dieta']:
                perfil.dietas.add(get_object_or_404(Dieta, nombre=dieta))
            return redirect('/product/list')
    return render(request, 'signUp.html', {'form': form})