from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.models import Perfil
from product.models import Producto, Ubicacion, UbicacionProducto, Dieta
from product.forms import ProductForm, ReporteForm, CreateProductForm, CreateNewUbication, ReviewProductForm
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from Eatsy import settings
import os
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def showProduct(request, productId):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=productId)
        if product.estado == 'Pendiente' and request.user.is_superuser:
            return render(request, 'products/show.html', {'product': product})
        elif product.estado == 'Aceptado':
            return render(request, 'products/show.html', {'product': product})
        else:
            messages.error(
                request, 'Los productos pendientes de revisión solo pueden ser vistos por el administrador.')
            return redirect('/admin')


def listProduct(request):

    if(request.user.is_superuser):
        products_list = Producto.objects.all()
    else:
        products_list = Producto.objects.filter(estado='Aceptado')

    # FILTRO
    # Para filtrar productos: ?dietas=1,2
    # Para mostrar todos los productos: ?dietas=
    # Sin ?dietas= muestra solo los productos que cumplan las dietas del usuario
    dietas = request.GET.get('dietas')
    if dietas == None:
        # Para el segundo sprint
        dietas_user = []
        for dieta in dietas_user:
            products_list = products_list.filter(dietas__id=dieta)
    elif dietas != '':
        for dieta in dietas.split(','):
            products_list = products_list.filter(dietas__id=dieta)

    # ORDEN
    #order = request.GET.get('order')
    # if order == 1:
    #    products_list.order_by()
    # else if order == 2:
    #    products_list.order_by()

    page = request.GET.get('page')
    paginator = Paginator(products_list, 10)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products/list.html', {'products': products})


def createProduct(request):
    form = CreateProductForm()
    return render(request, 'products/create.html', {'form': form})


def findProduct(request):
    if request.method == 'GET':
        form = ProductForm(request.GET, request.FILES)
        if form.is_valid():
            productName = form.cleaned_data['productName']
            if(request.user.is_superuser):
                filteredProducts = Producto.objects.filter(
                    titulo__icontains=productName)
            else:
                filteredProducts = Producto.objects.filter(
                    titulo__icontains=productName, estado='Aceptado')

            return render(request, 'products/list.html', {'products': filteredProducts})


def reportProduct(request, productId):
    producto = get_object_or_404(Producto, pk=productId)

    if request.method == 'GET':
        form = ReporteForm()
    elif request.method == 'POST':
        form = ReporteForm(request.POST)

        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.producto = Producto(id=productId)
            reporte.user = User(id=1)  # CORREGIR CUANDO HAYA LOGIN
            reporte.save()
            return redirect('product:show', producto.id)

    return render(request, 'products/addReport.html', {'form': form})

# TODO: Cuando esté el login cambiar el login_url
@user_passes_test(lambda u: u.is_superuser, login_url='/product/list')
def reviewProduct(request, productId):
    producto = get_object_or_404(Producto, pk=productId)
    # TODO: Revisar, ¿a dónde redirigir si intentan entrar por URL para revisar producto aceptado? No hay página de error
    if producto.estado == 'Aceptado':
        return redirect('product:list')
    else:
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
            if form.is_valid():
                # Si se ha aceptado
                if form.cleaned_data['revision'] == 'Aceptar':
                    producto.titulo = form.cleaned_data['nombre']
                    producto.descripcion = form.cleaned_data['descripcion']
                    producto.fecha = datetime.datetime.now()

                    path = default_storage.save(form.cleaned_data['foto'].name, ContentFile(form.cleaned_data['foto'].read()))
                    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
                    producto.foto = tmp_file
                    
                    # TODO: Revisar, se está poniendo el que llega en el formulario
                    producto.precioMedio = form.cleaned_data['precio']

                    # TODO: Revisar, se está metiendo en todas las ubicaciones el precio del formulario
                    # Si hay ubicación que no es supermercado se guarda
                    producto.ubicaciones.clear()
                    if(form.cleaned_data['nombreComercio'] != '' and form.cleaned_data['lat'] != '' and form.cleaned_data['lon'] != ''):
                        ubicacion = Ubicacion(
                            nombre=form.cleaned_data['nombreComercio'], latitud=form.cleaned_data['lat'], longitud=form.cleaned_data['lon'])
                        ubicacion.save()
                        # TODO: Adaptar el user cuando se haga el login
                        ubicacionProducto = UbicacionProducto(producto=producto, ubicacion=ubicacion, user=get_object_or_404(
                            Perfil, pk=1), precio=form.cleaned_data['precio'])
                        ubicacionProducto.save()

                    # Por cada supermercado crear tabla intermedia
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

        return render(request, 'products/review.html', {'form': form, 'product_id': productId})
