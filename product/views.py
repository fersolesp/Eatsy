from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect

from product.models import Producto
from product.forms import ProductForm, ReporteForm

# Create your views here.
def showProduct(request, productId):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=productId)
        return render(request, 'products/show.html', {'product': product})

def listProduct(request):
    products_list = Producto.objects.all()

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
            filteredProducts = Producto.objects.filter(titulo__icontains = productName)
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
            reporte.user = User(id=1) # CORREGIR CUANDO HAYA LOGIN
            reporte.save()
            return redirect('product:show', producto.id)

    return render(request, 'products/addReport.html', {'form': form})