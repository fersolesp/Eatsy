from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('show/<int:productId>', views.showProduct, name='show'),
    path('list', views.listProduct, name='list'),
    path('list/<slug:estado>', views.listProductByEstado, name='listState'),
    path('create', views.createProduct, name='create'),
    path('diet/add/<int:productId>', views.addDiet, name='addDiet'),
    path('report/<int:productId>', views.reportProduct, name='report'),
    path('review/<int:productId>', views.reviewProduct, name='review'),
    path('remove/<int:commentId>', views.removeComment, name='remove')
]