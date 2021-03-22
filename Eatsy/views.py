from django.shortcuts import render
# Create your views here.

def principalScreen(request):
     return render(request, 'products/paginaprincipal.html')