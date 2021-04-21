from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from recipe.models import Receta
from django.contrib.auth.decorators import user_passes_test, login_required

def  user_active_account(user):
    if user:
        return user.perfil.activeAccount
    return False

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def showReceta(request, recetaId):
    receta = get_object_or_404(Receta, pk=recetaId)
    return render(request, 'recipes/show.html', {'receta': receta})

