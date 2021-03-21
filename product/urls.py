from django.urls import path
from product import views

urlpatterns = [
    path('show/<int:productId>', views.showProduct),
    path('list', views.listProduct),
    path('list', views.findProduct)
]