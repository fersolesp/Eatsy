"""Eatsy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Eatsy import views
from django.conf.urls.static import static
from Eatsy import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('authentication/', include('authentication.urls')),
    path('', views.principalScreen),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "Eatsy.views.errorBadRequestView"
handler403 = "Eatsy.views.errorForbiddenView"
handler405 = "Eatsy.views.errorNotAllowedView"
handler410 = "Eatsy.views.errorGoneView"
handler404 = "Eatsy.views.errorNotFoundView"
handler500 = "Eatsy.views.errorServerErrorView"
