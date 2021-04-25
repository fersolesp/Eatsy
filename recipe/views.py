from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from recipe.models import Receta
from django.contrib.auth.decorators import user_passes_test, login_required
from recipe.forms import CreateRecipeForm
from product.models import Producto
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from authentication.models import Perfil

def  user_active_account(user):
    if user:
        return user.perfil.activeAccount
    return False

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def showReceta(request, recetaId):
    receta = get_object_or_404(Receta, pk=recetaId)
    return render(request, 'recipes/show.html', {'receta': receta})

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def createReceta(request):
    productos = Producto.objects.filter(estado="Aceptado").order_by('titulo')
    formProducts=[]
    for product in productos:
        formProducts.append((product.id,product.titulo)) 
    form = CreateRecipeForm(formProducts)
    if request.method=='GET':
        return render(request,'recipes/create.html', {'form':form})
    if request.method=='POST':
        form = CreateRecipeForm(formProducts,request.POST, request.FILES)
        if form.is_valid():
            path = default_storage.save(form.cleaned_data['imagen'].name, ContentFile(form.cleaned_data['imagen'].read()))
            nombre = form.cleaned_data["nombre"]
            descripcion = form.cleaned_data["descripcion"]
            perfil = get_object_or_404(Perfil, user=request.user)
            receta = Receta(nombre=nombre, descripcion=descripcion, imagen=path, perfil=perfil)
            receta.save()
            for producto in form.cleaned_data['productos']:
                receta.productos.add(producto)
            return redirect('recipe:show', receta.pk)
        else:
            return render(request,'recipes/create.html', {'form':form})

