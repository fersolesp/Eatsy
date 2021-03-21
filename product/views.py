from django.shortcuts import render, get_object_or_404
from product.models import Producto
from django.shortcuts import redirect
from django.contrib import messages
from product.forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def showProduct(request, productId):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=productId)
        if product.estado=='Pendiente' and request.user.is_superuser:
            return render(request, 'products/show.html', {'product': product})
        elif product.estado=='Aceptado':
            return render(request, 'products/show.html', {'product': product})
        else:
            messages.error(request,'Los productos pendientes de revisión solo pueden ser vistos por el administrador.')
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
    #if order == 1:
    #    products_list.order_by()
    #else if order == 2:
    #    products_list.order_by()

    page = request.GET.get('page')
    paginator = Paginator(products_list,10)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'products/list.html', {'products': products})


def findProduct(request):
    if request.method=='GET':
        form = ProductForm(request.GET, request.FILES)
        if form.is_valid():
            productName = form.cleaned_data['productName']
            if(request.user.is_superuser):
                filteredProducts = Producto.objects.filter(titulo__icontains = productName)
            else:
                filteredProducts = Producto.objects.filter(titulo__icontains = productName,estado='Aceptado')

            return render(request, 'products/list.html', {'products': filteredProducts})

