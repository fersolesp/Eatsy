from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('show/<int:productId>', views.showProduct, name='show'),
    path('list', views.listProduct, name='list'),
    path('listFind', views.findProduct, name='listFind'),
    path('create', views.createProduct, name='create'),
    path('report/<int:productId>', views.reportProduct, name='report'),
    path('review/<int:productId>', views.reviewProduct, name='review')
] 

