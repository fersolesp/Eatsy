from django.http import (HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseGone, HttpResponseNotAllowed)
from django.shortcuts import render
# Create your views here.

def principalScreen(request):
     return render(request, 'products/paginaprincipal.html')

def aboutUs(request):
     return render(request, 'products/aboutUs.html')

def contactUs(request):
     return render(request, 'products/contactUs.html')

def privacyPolicy(request):
     return render(request, 'products/privacyPolicy.html')

def errorNotFoundView(request,exception):
     return HttpResponseNotFound(render(request,"products/404.html"))

def errorServerErrorView(request):
     return HttpResponseServerError(render(request,"products/errorView.html"))

def errorBadRequestView(request,exception):
     return HttpResponseBadRequest(render(request,"products/errorView.html"))

def errorForbiddenView(request,exception):
     return HttpResponseForbidden(render(request,"products/errorView.html"))

def errorGoneView(request,exception):
     return HttpResponseGone(render(request,"products/errorView.html"))

def errorNotAllowedView(request,exception):
     return HttpResponseNotAllowed(render(request,"products/errorView.html"))



