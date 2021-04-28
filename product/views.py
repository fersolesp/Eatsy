from datetime import datetime

from authentication.models import Perfil
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from recipe.models import Receta
from shoppingList.models import ListaDeCompra

from product.forms import (AddUbicationForm, CommentForm, CreateProductForm,
                           ReporteForm, ReviewProductForm, SearchProductForm)
from product.models import (Aportacion, Dieta, Producto, Reporte, Ubicacion,
                            UbicacionProducto, Valoracion)


def aboutUs(request):
     return render(request, 'products/aboutUs.html')

def contactUs(request):
     return render(request, 'products/contactUs.html')

def privacyPolicy(request):
     return render(request, 'products/privacyPolicy.html')

def  user_active_account(user):
    if user:
        return user.perfil.activeAccount
    return False

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def showProduct(request, productId):
    product = get_object_or_404(Producto, pk=productId)
    valoracion=Valoracion.objects.filter(producto=product).aggregate(Avg('puntuacion'))["puntuacion__avg"]
    precio_medio=UbicacionProducto.objects.filter(producto=product).aggregate(Avg('precio'))["precio__avg"]
    valoracion_media=int(round(valoracion,0)) if valoracion!=None else 0
    aportaciones = Aportacion.objects.filter(producto=product)
    recetas= Receta.objects.filter(productos__in=[product]).distinct()
    if request.method == 'GET':
        form = ReporteForm()
        formComment= CommentForm()

        formUbicacion = AddUbicationForm()
        if product.estado=='Pendiente' and request.user.is_superuser:
            return render(request, 'products/show.html', {'product': product,'valoracion_media':valoracion_media,'precio_medio':precio_medio})
        elif product.estado=='Aceptado':
            return render(request, 'products/show.html', {'product': product,'valoracion_media':valoracion_media,'precio_medio':precio_medio, 'form':form,'formComment':formComment,'aportaciones':aportaciones,'recetas':recetas ,'formUbicacion' :formUbicacion})

        else:
            messages.error(
                request, 'Los productos pendientes de revisión solo pueden ser vistos por el administrador.')
            return redirect('/authentication/login')
    elif request.method == 'POST':
        if 'reportButton' in request.POST:
            form = ReporteForm(request.POST)
            formComment= CommentForm()
            formUbicacion = AddUbicationForm()
            formComment.empty_permitted=True
            if form.is_valid():
                reporte = form.save(commit=False)
                reporte.producto = Producto(id=productId)
                reporte.user = get_object_or_404(User, pk=request.user.pk)
                reporte.save()
                return redirect('product:show', product.id)
            else:
                return render(request, 'products/show.html', {'product': product,'valoracion_media':valoracion_media,'precio_medio':precio_medio, 'form':form,'formComment':formComment,'aportaciones':aportaciones,'recetas':recetas, 'formUbicacion' :formUbicacion})

        if 'commentButton' in request.POST:
            form = ReporteForm()
            formComment= CommentForm(request.POST)
            formUbicacion = AddUbicationForm()
            form.empty_permitted=True
            if formComment.is_valid():
                comentario = formComment.save(commit=False)
                comentario.producto = Producto(id=productId)
                comentario.user = get_object_or_404(Perfil, user=request.user)
                comentario.save()
                return redirect('product:show', product.id)
            else:
                return render(request, 'products/show.html', {'product': product,'valoracion_media':valoracion_media,'precio_medio':precio_medio,'form':form,'formComment':formComment,'aportaciones':aportaciones,'recetas':recetas ,'formUbicacion' :formUbicacion})
        if 'addingUbication' in request.POST:
            form = ReporteForm()
            formComment= CommentForm()
            formUbicacion = AddUbicationForm(request.POST)
            product = get_object_or_404(Producto, pk=productId)
            if formUbicacion.is_valid():
                ubicaciones = formUbicacion.cleaned_data['ubicaciones']
                nombre = formUbicacion.cleaned_data['nombreComercio']
                latitud = formUbicacion.cleaned_data['lat']
                longitud = formUbicacion.cleaned_data['lon']
                precio = formUbicacion.cleaned_data['precio']
                if(nombre!='' and latitud!='' and longitud!=''):
                    ubicacion = Ubicacion(nombre=nombre, latitud=latitud, longitud=longitud)
                    ubicacion.save()
                    ubicacionProducto = UbicacionProducto(producto=product, ubicacion=ubicacion, user=get_object_or_404(Perfil, user=request.user), precio = precio)
                    ubicacionProducto.save()
                else:
                    ubicacionProducto = UbicacionProducto(producto=product, ubicacion=ubicaciones, user=get_object_or_404(Perfil, user=request.user), precio=precio)
                    ubicacionProducto.save()

                return redirect('product:show', product.id)
            else:
                return render(request, 'products/show.html', {'product': product,'valoracion_media':valoracion_media,'precio_medio':precio_medio,'form':form,'formComment':formComment,'aportaciones':aportaciones, 'recetas':recetas, 'formUbicacion' :formUbicacion})

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def listProduct(request):
    product_list = Producto.objects.all()
    if not request.user.is_superuser:
        product_list = product_list.filter(estado='Aceptado')
    else:
        if request.GET.get('estado','') == "aceptado" or request.GET.get('estado','') == "pendiente":
            estado_get = "Aceptado" if request.GET["estado"] == "aceptado" else "Pendiente"
            product_list = product_list.filter(estado=estado_get)

    if request.GET & SearchProductForm.base_fields.keys():
        searchProductForm = SearchProductForm(request.GET)
    else:
        myDietas = Perfil.objects.get(user__id=request.user.id).dietas.all()
        searchProductForm = SearchProductForm({ 'dietas': myDietas })

    if searchProductForm.is_valid():
        # BUSCAR
        titulo = searchProductForm.cleaned_data['titulo']
        if titulo:
            product_list = product_list.filter(titulo__icontains = titulo)

        # FILTRAR
        for dieta in searchProductForm.cleaned_data['dietas']:
            product_list = product_list.filter(dietas__id = dieta.id)

        # UBICACIÓN
        for ubicacion in searchProductForm.cleaned_data['ubicaciones']:
            product_list = product_list.filter(ubicaciones__id = ubicacion.id)
        print(searchProductForm.cleaned_data)

        # ORDENAR
        orderBy = searchProductForm.cleaned_data['orderBy']
        if orderBy:
            product_list = product_list.order_by(orderBy)
    
    page = request.GET.get('page')
    paginator = Paginator(product_list, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
        messages.error(request, 'Superior a la paginación existente, Se muestra la última página ('+str(paginator.num_pages)+')')

    return render(request, 'products/list.html', {
        'products': products, 'searchProductForm': searchProductForm
        })

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def createProduct(request):
    if request.method=='GET':
        form=CreateProductForm()
        return render(request,'products/create.html', {'form':form})
    if request.method=='POST':
        form=CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['ubicaciones'] == None and form.cleaned_data['nombreComercio']=="":
                form.errors.nombreComercio = "El campo Nombre del Comercio no puede estar vacío si añade una ubicación nueva"
                return render(request,'products/create.html', {'form':form})
            path = default_storage.save(form.cleaned_data['foto'].name, ContentFile(form.cleaned_data['foto'].read()))
            
            nombre = form.cleaned_data["nombre"]
            descripcion = form.cleaned_data["descripcion"]
            precio = form.cleaned_data["precio"]
            dieta = form.cleaned_data['dieta']
            ubicacion = form.cleaned_data['ubicaciones']
            
            producto = Producto(titulo = nombre, descripcion = descripcion, foto = path, precioMedio = precio, estado = "Pendiente",user = get_object_or_404(Perfil, user=request.user))
            producto.save()

            for d in dieta:
                producto.dietas.add(get_object_or_404(Dieta, nombre=d))

            # Por cada pequemercado crear tabla intermedia
            if(form.cleaned_data['nombreComercio']!='' and form.cleaned_data['lat']!='' and form.cleaned_data['lon']!=''):
                ubicacion = Ubicacion(nombre=form.cleaned_data['nombreComercio'], latitud=form.cleaned_data['lat'], longitud=form.cleaned_data['lon'])
                ubicacion.save()
                ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, user=request.user), precio = precio)
                ubicacionProducto.save()
                
            # Por cada supermercado crear tabla intermedia
            else:
                ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, user=request.user), precio=form.cleaned_data['precio'])
                ubicacionProducto.save()

            producto.save()

            return redirect('product:list')
        else:
            return render(request,'products/create.html', {'form':form})


@user_passes_test(lambda u: u.is_superuser, login_url='/authentication/login') # Nuevo Log In
def reviewProduct(request, productId):
    producto = get_object_or_404(Producto, pk=productId)
    if request.method == 'GET':
        data = {
            'foto': producto.foto,
            'nombre': producto.titulo,
            'descripcion': producto.descripcion,
            'precio': producto.precioMedio,
            'dieta': producto.dietas.all(),
            'ubicaciones': producto.ubicaciones.all()
        }
        form = ReviewProductForm(initial=data)

    elif request.method == 'POST':
        form = ReviewProductForm(request.POST, request.FILES)
        if form.is_valid():

            # # Comprobamos en el caso de que sea ubicacion de mapa que el nombre no sea vacío
            # if form.cleaned_data['ubicaciones'] == None and form.cleaned_data['nombreComercio']=='':
            #     form.errors.nombreComercio = 'El campo Nombre del Comercio no puede estar vacío si añade una ubicación nueva'
            #     return render(request, 'products/review.html', {'form': form, 'product_id': productId, 'producto':producto})

            # Si se ha aceptado
            if form.cleaned_data['revision'] == 'Aceptar':
                producto.titulo = form.cleaned_data['nombre']
                producto.descripcion = form.cleaned_data['descripcion']
                producto.fecha = datetime.now()

                if(form.cleaned_data['foto'] != None):
                    path = default_storage.save(form.cleaned_data['foto'].name, ContentFile(form.cleaned_data['foto'].read()))
                    producto.foto = path

                # Si hay ubicación que no es supermercado se guarda
                # if(form.cleaned_data['nombreComercio'] != '' and form.cleaned_data['lat'] != '' and form.cleaned_data['lon'] != ''):
                #     ubicacion = Ubicacion(
                #         nombre=form.cleaned_data['nombreComercio'], latitud=form.cleaned_data['lat'], longitud=form.cleaned_data['lon'])
                #     ubicacion.save()
                #     ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(
                #         Perfil, pk=1), precio=form.cleaned_data['precio'])
                #     ubicacionProducto.save()

                # Por cada supermercado crear tabla intermedia
                producto.ubicaciones.clear()
                for ubicacion in form.cleaned_data['ubicaciones']:
                    ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, user=request.user), precio=form.cleaned_data['precio'])
                    ubicacionProducto.save()

                # Guardar las dietas
                producto.dietas.clear()
                for dieta in form.cleaned_data['dieta']:
                    producto.dietas.add(get_object_or_404(Dieta, nombre=dieta))

                producto.estado = 'Aceptado'
                producto.save()
                return redirect('product:show', producto.id)

            # Si se ha descartado se borra el producto
            else:
                producto.delete()
                return redirect('product:list')

    return render(request, 'products/review.html', {'form': form, 'product_id': productId, 'producto':producto})

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def rateProduct(request, productId):
    if request.method == 'POST':
        idProd = request.POST.get('id')
        rate = request.POST.get('rate')

        numValoraciones = Valoracion.objects.filter(user=get_object_or_404(Perfil, user=request.user), producto=get_object_or_404(Producto, pk=idProd)).count()
        if numValoraciones>=1:
             return JsonResponse({'success':'false', 'msj': "Ya ha realizado una valoración"}, safe=False)
        else:
            valoracion = Valoracion(puntuacion = rate, fecha = datetime.now(), user =get_object_or_404(Perfil, user=request.user), producto = get_object_or_404(Producto, pk=idProd))
            valoracion.save()
            return JsonResponse({'success':'true', 'msj': "Su voto ha sido procesado"}, safe=False)

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def removeComment (request, commentId):
    comment = get_object_or_404(Aportacion, pk=commentId)
    product_id = comment.producto.id
    if comment.user.user.pk == request.user.pk:
        comment.delete()
    else:
        raise Http404

    return redirect('product:show', product_id)

@user_passes_test(lambda u: u.is_superuser, login_url='/authentication/login') # Nuevo Log In
def listReports(request):
    reports_list = Reporte.objects.filter(estado='Pendiente')

    page = request.GET.get('page')
    paginator = Paginator(reports_list,12)

    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    
    return render(request, 'reports/list.html', { 'reports': reports })


@user_passes_test(lambda u: u.is_superuser, login_url='/authentication/login') # Nuevo Log In
def reviewReport(request, reporteId):

    if request.method == 'POST':

        reporte = get_object_or_404(Reporte, pk=reporteId)
        if request.POST['revision'] == 'No Procede':
            reporte.estado = 'No procede'
            reporte.save()

        elif request.POST['revision'] == 'Resuelto':
            reporte.estado = 'Resuelto'
            product = reporte.producto
            product.estado = "Pendiente"
            product.save()
            reporte.save()

        return redirect("/product/report/list")

@login_required(login_url='/authentication/login')
@user_passes_test(user_active_account, login_url='/authentication/create-subscription')
def addProductToShoppingList(request):
    if request.method == 'POST':
        idProd = request.POST.get('productId')
        producto = get_object_or_404(Producto.objects.filter(pk=idProd))        
        listaCompra = ListaDeCompra.objects.filter(perfil=get_object_or_404(Perfil, user=request.user))
        if listaCompra.exists():
            lista = listaCompra.get()
            if producto.listadecompra_set.filter(pk=lista.pk).exists():
                return JsonResponse({'success':'false', 'msj': "No se puede añadir a la lista de la compra porque el producto ya se encuentra en la misma"}, safe=False)
            else:
                listaCompra.get().productos.add(producto)
                return JsonResponse({'success':'true', 'msj': "El producto se ha añadido correctamente a la lista de la compra"}, safe=False)
            
        else:
            lista = ListaDeCompra(perfil=get_object_or_404(Perfil, user=request.user))
            lista.save()
            lista.productos.add(producto)
            return JsonResponse({'success':'true', 'msj': "El producto se ha añadido correctamente a la lista de la compra"}, safe=False)               
