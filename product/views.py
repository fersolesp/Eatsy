from django.shortcuts import render, get_object_or_404
from product.models import Producto
from product.forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def showProduct(request, productId):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=productId)
        return render(request, 'products/show.html', {'product': product})

def listProduct(request):

    products_list = Producto.objects.all()

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
