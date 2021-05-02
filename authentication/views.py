#from django.shortcuts import render
import json
import os

import stripe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import \
    login_required  # , staff_member_required, user_passes_test #Usar estos métodos para controlar quién puede acceder a las vistas
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from dotenv import load_dotenv

#Para comprobar si es superuser, poner @user_passes_test(lambda u: u.is_superuser) antes de definir la vista. Con el resto bastaría poner @login_required o @staff_member_required
from authentication.forms import (LoginForm, ProfileForm, SignUpForm,
                                  resetPasswordForm)
from authentication.models import Dieta, Perfil

load_dotenv('AWS.env')
stripe.api_key = os.environ.get('STRIPE_API_KEY')

def updateUserSubscriptionState(user):
    load_dotenv('AWS.env')
    stripe.api_key = os.environ.get('STRIPE_API_KEY')

    active = False
    customer = stripe.Customer.list(email=user.email)
    if customer:
        customer = customer['data'][0]

        for subscription in stripe.Subscription.list(customer=customer['id'], status='all')['data']:
            if subscription['status'] in ['active', 'trialing']:
                active = True
                break

    perfil = Perfil.objects.get(user__id=user.id)
    perfil.activeAccount = active
    perfil.save()

    return active

def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

@login_excluded('../')
def loginPage(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if updateUserSubscriptionState(user):
                    return redirect('/product/list')
                else:
                    return redirect('authentication:profile')
            else:
                form.add_error('password', 'Inicio de sesión incorrecto')
                return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':form})

@login_excluded('../')
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

@login_required(login_url='/authentication/login')
def myProfile(request):
    user = request.user
    perfil = get_object_or_404(Perfil, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellidos']
            user.save()
            perfil.dietas.clear()
            for dieta in form.cleaned_data['dieta']:
                perfil.dietas.add(get_object_or_404(Dieta, nombre=dieta))
            perfil.save()
        else:
            return render(request, 'perfil.html', {'form': form})
    data = {
            'nombre': user.first_name,
            'apellidos': user.last_name,
            'dieta': [dieta.nombre for dieta in perfil.dietas.all()],
            'activada': perfil.activeAccount
        }
    form = ProfileForm(initial=data)
    return render(request, 'perfil.html', {'form': form})

@login_required(login_url='/authentication/login')
def resetPassword(request):
    user = request.user
    form = resetPasswordForm()
    if request.method == 'POST':
        form = resetPasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=user, password=form.cleaned_data['password'])
            if user is not None:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                return redirect('/authentication/profile')
            else:
                form.add_error('password', 'Contraseña incorrecta')
                return render(request, 'resetPass.html', {'form':form})
    return render(request, 'resetPass.html', {'form': form})

@login_required(login_url='/authentication/login')
@csrf_protect
def create_customer(request):
    load_dotenv('AWS.env')
    stripe.api_key = os.environ.get('STRIPE_API_KEY')
    if request.method == 'POST':
        # Reads application/json and returns a response
        try:
            customer = stripe.Customer.list(email=request.user.email)
            if not customer:
                # Create a new customer object
                customer = stripe.Customer.create(email=request.user.email)
            else:
                customer = customer["data"][0]

            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.
            resp = JsonResponse({'customer':customer})

            return resp
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

@login_required(login_url='/authentication/login')
def createSubscription(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
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
            trial = len(stripe.Subscription.list(customer=data['customerId'], status='all')['data']) == 0
            if trial:
                subscription = stripe.Subscription.create(
                    customer=data['customerId'],
                    items=[
                        {
                            'price': data['priceId']
                        }
                    ],
                    expand=['latest_invoice.payment_intent'],
                    trial_period_days=30
                )
            else:
                subscription = stripe.Subscription.create(
                    customer=data['customerId'],
                    items=[
                        {
                            'price': data['priceId']
                        }
                    ],
                    expand=['latest_invoice.payment_intent']
                )

            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=200)
    elif request.method == 'GET':
        if request.user.perfil.activeAccount == False:
            return render(request, 'subscribe.html')
        else:
            return redirect("product:list")

@login_required(login_url='/authentication/login')
def cancelSubscription(request):
    if request.method == 'POST':
        try:
            customer = stripe.Customer.list(email=request.user.email)
            if not customer:
                return JsonResponse(error={'message': "El cliente para el que se quiere cancelar la suscripción no existe."}), 200
            else:
                for subscription in stripe.Subscription.list(customer=customer["data"][0]["id"])['data']:
                    subscriptionId = subscription['id']
                    # delete the subscription
                    stripe.Subscription.delete(subscriptionId)
                perfil = Perfil.objects.get(user__id=request.user.id)
                perfil.activeAccount = False
                perfil.save()
                return JsonResponse(customer)
        except Exception as e:
            return JsonResponse(error={'message': str(e)}), 200
    elif request.method == 'GET':
        return render(request, 'login.html')

@csrf_protect
@login_required(login_url='/authentication/login')
def update_access(request):
    if request.method == 'POST':
        updateUserSubscriptionState(request.user)
        return JsonResponse({}, status=200)
