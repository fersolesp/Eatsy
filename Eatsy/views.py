from django.shortcuts import render
# Create your views here.

def principalScreen(request):
     return render(request, 'products/paginaprincipal.html')

def subscribe(request):
     return render(request,'products/subscribe.html')