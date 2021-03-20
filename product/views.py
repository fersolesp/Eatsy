from django.shortcuts import render, get_object_or_404
from product.models import Producto

# Create your views here.

def showProduct(request, productId):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=productId)
        return render(request, 'products/show.html', {'product': product})
