#from django.shortcuts import render
from django.contrib.auth.decorators import login_required #, staff_member_required, user_passes_test #Usar estos métodos para controlar quién puede acceder a las vistas
#Para comprobar si es superuser, poner @user_passes_test(lambda u: u.is_superuser) antes de definir la vista. Con el resto bastaría poner @login_required o @staff_member_required
from authentication.forms import SignUpForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from authentication.models import Perfil, Dieta
import json, stripe
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv('STRIPE_API_KEY')

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

def showProfile(request):
    usuario = request.user
    perfil = Perfil.objects.filter(user=usuario)
    if usuario.is_authenticated:
        return render(request, 'perfil.html', {'usuario': usuario, 'perfil': perfil})
    else:
        return redirect('/authentication/login')

def createSubscription(request):
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=data['customerId'],
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                data['customerId'],
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            # Create the subscription
            subscription = stripe.Subscription.create(
                customer=data['customerId'],
                items=[
                    {
                        'price': 'price_HGd7M3DV3IMXkC'
                    }
                ],
                expand=['latest_invoice.payment_intent'],
            )
            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse(error={'message': str(e)}), 200
    elif request.method == 'GET':
        return render(request, 'subscribe.html')

