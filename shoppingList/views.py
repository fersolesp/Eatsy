from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from product.models import Producto
from recipe.models import Receta

from shoppingList.models import ListaDeCompra


def  user_active_account(user):
    if user:
        return user.perfil.activeAccount
    return False

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def show(request):
    try:
        lista  = ListaDeCompra.objects.get(perfil=request.user.perfil)
        return render(request, 'shoppingList/show.html', { 'shoppingList': lista })
    except ListaDeCompra.DoesNotExist:
        return render(request, 'shoppingList/show.html', { 'shoppingList': None })

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def removeProduct(request, productId):
    try:
        lista  = ListaDeCompra.objects.get(perfil=request.user.perfil)
        lista.productos.remove(productId)
    except:
        pass

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def empty(request):
    try:
        lista  = ListaDeCompra.objects.get(perfil=request.user.perfil)
        lista.productos.clear()
        lista.save()
    except:
        pass
    return redirect('shoppingList:show')
