from django.shortcuts import render, get_object_or_404
from product.models import Producto
from django.shortcuts import redirect
from django.contrib import messages
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
    
    print(products_list)
    page = request.GET.get('page')
    paginator = Paginator(products_list,10)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'products/list.html', {'products': products})
