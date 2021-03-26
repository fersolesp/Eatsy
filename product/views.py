import datetime
import os
from datetime import datetime

from authentication.models import Perfil
from product.models import Producto, Ubicacion, UbicacionProducto, Dieta, Valoracion, Aportacion, Reporte
from product.forms import ReporteForm, CreateProductForm, ReviewProductForm, CommentForm, SearchProductForm, AddUbicationForm, ReviewReporteForm
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from Eatsy import settings

from product.forms import (AddUbicationForm, ChangeRequestForm, CommentForm,
                           CreateProductForm, ReporteForm, ReviewProductForm,
                           SearchProductForm)
from product.models import (Aportacion, ChangeRequest, Dieta, Producto,
                            Reporte, Ubicacion, UbicacionProducto, Valoracion)

def get_product_or_404(request, id):
    """
    Si el producto no existe o está pendiente de revisión (y el usuario no es superuser),
    devuelve error 404.
    """
    product = get_object_or_404(Producto, pk=id)
    if product.estado == 'Pendiente' and not request.user.is_superuser:
        raise Http404()
    return product

def showProduct(request, productId):
    product = get_object_or_404(Producto, pk=productId)
    if request.method == 'GET':
        form = ReporteForm()
        formComment= CommentForm()
        if product.estado=='Pendiente' and request.user.is_superuser:
            return render(request, 'products/show.html', {'product': product})
        elif product.estado=='Aceptado':
            return render(request, 'products/show.html', {'product': product, 'form':form,'formComment':formComment})
        else:
            messages.error(
                request, 'Los productos pendientes de revisión solo pueden ser vistos por el administrador.')
            return redirect('/admin')
    elif request.method == 'POST':
        form = ReporteForm(request.POST)
        formComment= CommentForm()
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.producto = Producto(id=productId)
            reporte.user = User(id=1) # TODO: CORREGIR CUANDO HAYA LOGIN
            reporte.save()
            return render(request, 'products/show.html', {'product': product,'msj': '¡Gracias! Se ha recibido correctamente el reporte. ', 'form':form,'formComment':formComment})
        else:
            return redirect('product:show', product.id)   

def listProduct(request):
    product_list = Producto.objects.all()
    if not request.user.is_superuser:
        product_list = product_list.filter(estado='Aceptado')
    else:
        if request.GET.get('estado','') == "aceptado" or request.GET.get('estado','') == "pendiente":
            estado_get = "Aceptado" if request.GET["estado"] == "aceptado" else "Pendiente"
            product_list = product_list.filter(estado=estado_get)
    
    if request.GET:
        searchProductForm = SearchProductForm(request.GET)
        # BUSCAR
        if searchProductForm.data.get("titulo"):
            titulo = searchProductForm.data['titulo']
            product_list = product_list.filter(titulo__icontains = titulo)

        # FILTRAR
        if searchProductForm.data.get('dietas'):
            for dieta in searchProductForm.data['dietas']:
                product_list = product_list.filter(dietas__id = dieta)

        # ORDENAR
        if searchProductForm.data.get('orderBy'):
            if searchProductForm.data.get('orderBy') in ["id","-id","precioMedio","-precioMedio"]:
                product_list = product_list.order_by(searchProductForm.data['orderBy'])
    
    else:
        # Si el formulario no se ha enviado, rellenar con valores por defecto
        # SPRINT 2 #
        searchProductForm = SearchProductForm()
    
    page = request.GET.get('page')
    paginator = Paginator(product_list, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products/list.html', {
        'products': products, 'searchProductForm': searchProductForm
        })

def listProductByEstado(request, estado):
    if(estado.lower() == "aceptado"):
        estado = "Aceptado"
    else:
        estado = "Pendiente"

    products_list = Producto.objects.filter(estado=estado)

    page = request.GET.get('page')
    paginator = Paginator(products_list,12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'products/list.html', { 'products': products })


def createProduct(request):
    if request.method=='GET':
        form=CreateProductForm()
        return render(request,'products/create.html', {'form':form})
    if request.method=='POST':
        form=CreateProductForm(request.POST, request.FILES)
        print(form.errors)
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
            
            producto = Producto(titulo = nombre, descripcion = descripcion, foto = path, precioMedio = precio, estado = "Pendiente",user = get_object_or_404(Perfil, pk=2))
            producto.save()

            for d in dieta:
                producto.dietas.add(get_object_or_404(Dieta, nombre=d))

            # Por cada pequemercado crear tabla intermedia
            if(form.cleaned_data['nombreComercio']!='' and form.cleaned_data['lat']!='' and form.cleaned_data['lon']!=''):
                ubicacion = Ubicacion(nombre=form.cleaned_data['nombreComercio'], latitud=form.cleaned_data['lat'], longitud=form.cleaned_data['lon'])
                ubicacion.save()
                # TODO: Adaptar el user cuando se haga el login
                ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, pk=2), precio = precio)
                ubicacionProducto.save()
                
            # Por cada supermercado crear tabla intermedia
            else:
                # TODO: Adaptar el user cuando se haga el login
                ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(
                    Perfil, pk=2), precio=form.cleaned_data['precio'])
                ubicacionProducto.save()

            producto.save()

            return redirect('product:list')
        else:
            return render(request,'products/create.html', {'form':form})

    

          
def addUbication(request, productId):
    if request.method == 'GET':
        form = AddUbicationForm()
        return render(request,'products/show.html', {'form':form})

    if request.method == 'POST':
        form=AddUbicationForm(request.POST, request.FILES)

        if form.is_valid():
            ubicaciones = form.cleaned_data['ubicaciones']
            nombre = form.cleaned_data['nombreComercio']
            latitud = form.cleaned_data['lat']
            longitud = form.cleaned_data['lon']
            precio = form.cleaned_data['precio']
            producto = get_object_or_404(Producto, pk=productId)

            if(nombre!='' and latitud!='' and longitud!=''):
                ubicacion = Ubicacion(nombre=nombre, latitud=latitud, longitud=longitud)
                ubicacion.save()

                # TODO: Adaptar el user cuando se haga el login
                ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, pk=2), precio = precio)
                ubicacionProducto.save()

            for ubicacion in ubicaciones:
                # TODO: Adaptar el user cuando se haga el login
                ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(Perfil, pk=2), precio=precio)
                ubicacionProducto.save()

            return render (request,'products/show.html')

        else:
            return render(request,'products/show.html', {'form':form})


def reportProduct(request, productId):
    producto = get_object_or_404(Producto, pk=productId)

    if request.method == 'GET':
        form = ReporteForm()
    elif request.method == 'POST':
        form = ReporteForm(request.POST)

        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.producto = Producto(id=productId)
            reporte.user = User(id=1)  # TODO: CORREGIR CUANDO HAYA LOGIN
            reporte.save()
            return redirect('product:show', producto.id)

    return render(request, 'products/addReport.html', {'form': form})


# TODO: Cuando esté el login cambiar el login_url
@user_passes_test(lambda u: u.is_superuser, login_url='/product/list')
def showReport(request, reportId):
    reporte = get_object_or_404(Reporte, pk=reportId)
    return render(request, 'products/list.html', {'report': reporte})


# TODO: Cuando esté el login cambiar el login_url
@user_passes_test(lambda u: u.is_superuser, login_url='/product/list')
def reviewProduct(request, productId):
    producto = get_object_or_404(Producto, pk=productId)
    # TODO: Revisar, ¿a dónde redirigir si intentan entrar por URL para revisar producto aceptado? No hay página de error
    if request.method == 'GET':
        data = {
            'foto': producto.foto,
            'nombre': producto.titulo,
            'descripcion': producto.descripcion,
            'precio': producto.precioMedio,
            'dieta': [dieta.nombre for dieta in producto.dietas.all()],
            'ubicaciones': producto.ubicaciones.all()
        }
        form = ReviewProductForm(initial=data)

    elif request.method == 'POST':
        form = ReviewProductForm(request.POST, request.FILES)
        print('Errores: ', form.errors)
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
                #     # TODO: Adaptar el user cuando se haga el login
                #     ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(
                #         Perfil, pk=1), precio=form.cleaned_data['precio'])
                #     ubicacionProducto.save()

                # Por cada supermercado crear tabla intermedia
                producto.ubicaciones.clear()
                for ubicacion in form.cleaned_data['ubicaciones']:
                    # TODO: Adaptar el user cuando se haga el login
                    ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(
                        Perfil, pk=1), precio=form.cleaned_data['precio'])
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


def rateProduct(request, productId):
    if request.method == 'POST':
        id = request.POST.get('id')
        rate = request.POST.get('rate')
        # TODO: Adaptar el user cuando se haga el login
        
        numValoraciones = Valoracion.objects.filter(user=get_object_or_404(Perfil, pk=2), producto=get_object_or_404(Producto, pk=id)).count()
        if numValoraciones>=1:
             return JsonResponse({'success':'false', 'msj': "Ya ha realizado una valoración"}, safe=False)
        else:
            valoracion = Valoracion(puntuacion = rate, fecha = datetime.now(), user =get_object_or_404(
                            Perfil, pk=2), producto = get_object_or_404(Producto, pk=id))
            valoracion.save()
            return JsonResponse({'success':'true', 'msj': "Su voto ha sido procesado"}, safe=False)

def commentProduct(request, productId):
    producto = get_object_or_404(Producto, pk=productId)

    if request.method == 'GET':
        form = CommentForm()
    elif request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.producto = Producto(id=productId)
            comentario.user = Perfil(pk=1)  # CORREGIR CUANDO HAYA LOGIN
            comentario.save()
            return redirect('product:show', producto.id)

    return render(request, 'products/addReport.html', {'form': form})

def removeComment (request, commentId):
    comment = get_object_or_404(Aportacion, pk=commentId)
    if comment.user.user.pk == request.user.pk:
        comment.delete()
    else:
        # TODO: redirigir a pantalla de error cuando esté
        return redirect('product:list')

    return render(request, 'products/show.html')

def requestChange(request, productId):
    if request.user.is_superuser:
        return redirect(f'/admin/product/producto/{productId}/change/') # TODO: creo que se puede mejorar

    product = get_product_or_404(request, productId)

    if request.POST:
        changeRequestForm = ChangeRequestForm(request.POST)

        if changeRequestForm.is_valid():
            dietas = changeRequestForm.cleaned_data['dietas'].all()

            # Se creará si hay cambios con respecto a las dietas del producto
            if set(dietas) != set(product.dietas.all()):
                # Se creará si no hay otra petición con las mismas características
                changeRequests = ChangeRequest.objects.annotate(count=Count('dietas')).filter(count=len(dietas))
                for dieta in dietas:
                    changeRequests.filter(dietas__id=dieta.id)

                if len(changeRequests) == 0:
                    changeRequest = ChangeRequest()
                    changeRequest.product = Producto(id=product.id)
                    changeRequest.creation_user = User(id=1)  # TODO: CORREGIR CUANDO HAYA LOGIN
                    changeRequest.save()

                    changeRequest.dietas.add(*dietas)
                    changeRequest.save()
                return redirect('product:show', product.id)
            else:
                changeRequestForm.add_error('dietas', 'Has seleccionado las mismas dietas que ya tenía el producto.')
    else:
        changeRequestForm = ChangeRequestForm(initial={ 'dietas': product.dietas.all() })

    return render(request, 'products/requestChange.html', { 'product': product, 'changeRequestForm': changeRequestForm })

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def listChangeRequests(request):
    changeRequests =  ChangeRequest.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(changeRequests, 20)

    try:
        changeRequests = paginator.page(page)
    except PageNotAnInteger:
        changeRequests = paginator.page(1)
    except EmptyPage:
        changeRequests = paginator.page(paginator.num_pages)

    return render(request, 'products/changeRequest/list.html', { 'changeRequests': changeRequests })

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def acceptChangeRequest(request, changeRequestId):
    changeRequest = get_object_or_404(ChangeRequest, pk=changeRequestId)
    changeRequest.apply()

    return redirect('product:listChangeRequests')   

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def rejectChangeRequest(request, changeRequestId):
    changeRequest = get_object_or_404(ChangeRequest, pk=changeRequestId)
    changeRequest.delete()

    return redirect('product:listChangeRequests')   

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def listReports(request):
    reports_list = Reporte.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(reports_list,12)

    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    
    return render(request, 'reports/list.html', { 'reports': reports })


@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def reviewReport(request, reporteId):
    reporte = get_object_or_404(Reporte, pk=reporteId)

    if request.method == 'GET':
        data = {
            'causa': reporte.causa,
            'comentario': reporte.comentario, 
            'revision': reporte.estado,
        }
        form = ReviewReporteForm(initial=data)

    elif request.method == 'POST':
        form = ReviewReporteForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['revision'] == 'No Procede':
                reporte.estado = 'No Procede'
                reporte.save()

            elif form.cleaned_data['revision'] == 'Resuelto':
                reporte.estado = 'Resuelto'
                reporte.save()

            return render(request, 'products/show.html')

    return render(request, 'products/show.html', {'form': form, 'reporte': reporte})
  