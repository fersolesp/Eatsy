from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from recipe.models import Receta
from django.contrib.auth.decorators import user_passes_test, login_required
from recipe.forms import CreateRecipeForm
from product.models import Producto

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
    if request.method=='GET':
        form = CreateRecipeForm()
        return render(request,'recipes/create.html', {'form':form})

    # TODO: el controlador de crear recetita - Javi :p
    # está copiado de producto, simplemente; hay que arreglar el botón de elegir la foto, no cómo se pone :S

    # if request.method=='POST':
    #     form=CreateProductForm(request.POST, request.FILES)
    #     print(form.errors)
    #     if form.is_valid():
    #         if form.cleaned_data['ubicaciones'] == None and form.cleaned_data['nombreComercio']=="":
    #             form.errors.nombreComercio = "El campo Nombre del Comercio no puede estar vacío si añade una ubicación nueva"
    #             return render(request,'products/create.html', {'form':form})
    #         path = default_storage.save(form.cleaned_data['foto'].name, ContentFile(form.cleaned_data['foto'].read()))
            
    #         nombre = form.cleaned_data["nombre"]
    #         descripcion = form.cleaned_data["descripcion"]
    #         precio = form.cleaned_data["precio"]
    #         dieta = form.cleaned_data['dieta']
    #         ubicacion = form.cleaned_data['ubicaciones']
            
    #         producto = Producto(titulo = nombre, descripcion = descripcion, foto = path, precioMedio = precio, estado = "Pendiente",user = get_object_or_404(Perfil, user=request.user))
    #         producto.save()

    #         for d in dieta:
    #             producto.dietas.add(get_object_or_404(Dieta, nombre=d))

    #         # Por cada pequemercado crear tabla intermedia
    #         if(form.cleaned_data['nombreComercio']!='' and form.cleaned_data['lat']!='' and form.cleaned_data['lon']!=''):
    #             ubicacion = Ubicacion(nombre=form.cleaned_data['nombreComercio'], latitud=form.cleaned_data['lat'], longitud=form.cleaned_data['lon'])
    #             ubicacion.save()
    #             ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, user=request.user), precio = precio)
    #             ubicacionProducto.save()
                
    #         # Por cada supermercado crear tabla intermedia
    #         else:
    #             ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, user=request.user), precio=form.cleaned_data['precio'])
    #             ubicacionProducto.save()

    #         producto.save()

    #         return redirect('product:list')
    #     else:
    #         return render(request,'products/create.html', {'form':form})

