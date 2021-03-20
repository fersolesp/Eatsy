from django.shortcuts import render, get_object_or_404
from product.models import Producto
from django.shortcuts import redirect
from django.contrib import messages

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
