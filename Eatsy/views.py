from django.shortcuts import render
from django.http import (HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseGone, HttpResponseNotAllowed)
from product.forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.

def principalScreen(request):
     return render(request, 'products/paginaprincipal.html')

def errorNotFoundView(request,exception):
     return HttpResponseNotFound(render(request,"products/404.html"))

def errorServerErrorView(request):
     return HttpResponseServerError(render(request,"products/errorView.html"))

def errorBadRequestView(request,exception):
     return HttpResponseBadRequest(render(request,"products/errorView.html"))

def errorForbiddenView(request,exception):
     return HttpResponseForbidden(render(request,"products/errorView.html"))

def errorGoneView(request,exception):
     return HttpResponseGone(render(request,"products/errorView.html"))

def errorNotAllowedView(request,exception):
     return HttpResponseNotAllowed(render(request,"products/errorView.html"))

def subscribe(request):
     return render(request,'products/subscribe.html')

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
        return render(request, 'products/login.html', {'form':form} )

