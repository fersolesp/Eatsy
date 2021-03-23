from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from product.models import Producto
from product.forms import SearchProductForm, ReporteForm, CreateProductForm

# Create your views here.

def showProduct(request, productId):
    product = get_object_or_404(Producto, pk=productId)
    if request.method == 'GET':
        form = ReporteForm()
        if product.estado=='Pendiente' and request.user.is_superuser:
            return render(request, 'products/show.html', {'product': product})
        elif product.estado=='Aceptado':
            return render(request, 'products/show.html', {'product': product, 'form':form})
        else:
            messages.error(request,'Los productos pendientes de revisión solo pueden ser vistos por el administrador.')
            return redirect('/admin')
    elif request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.producto = Producto(id=productId)
            reporte.user = User(id=1) # CORREGIR CUANDO HAYA LOGIN
            reporte.save()
            return render(request, 'products/show.html', {'product': product,'msj': '¡Gracias! Se ha recibido correctamente el reporte. ', 'form':form})
        else:
            return redirect('product:show', product.id)   

def listProduct(request):
    product_list = Producto.objects.all()
    if not request.user.is_superuser:
        product_list = product_list.filter(estado='Aceptado')

    if request.GET & SearchProductForm.base_fields.keys():
        searchProductForm = SearchProductForm(request.GET)
    else:
        # Si el formulario no se ha enviado, rellenar con valores por defecto
        # SPRINT 2 #
        initial = { 'dietas': [] } # poner lista de ID o lista de Dieta
        searchProductForm = SearchProductForm(initial = initial)

    if searchProductForm.is_valid():
        # BUSCAR
        titulo = searchProductForm.cleaned_data['titulo']
        if titulo:
            product_list = product_list.filter(titulo__icontains = titulo)

        # FILTRAR
        for dieta in searchProductForm.cleaned_data['dietas']:
            product_list = product_list.filter(dietas__id = dieta.id)

        # ORDENAR
        product_list = product_list.order_by(searchProductForm.cleaned_data['orderBy'])

    for producto in product_list:
        print(producto.titulo)

    page = request.GET.get('page')
    paginator = Paginator(product_list, 12)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'products/list.html', { 'products': products, 'searchProductForm': searchProductForm })

  
def createProduct(request):
    form = CreateProductForm()
    return render(request,'products/create.html', {'form':form})