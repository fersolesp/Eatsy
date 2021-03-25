from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('show/<int:productId>', views.showProduct, name='show'),
    path('list', views.listProduct, name='list'),
    path('list/<slug:estado>', views.listProductByEstado, name='listState'),
    path('create', views.createProduct, name='create'),
    path('report/<int:productId>', views.reportProduct, name='report'),
    path('review/<int:productId>', views.reviewProduct, name='review'),
    path('remove/<int:commentId>', views.removeComment, name='remove'),
    path('<int:productId>/requestChange', views.requestChange, name='requestChange'),
    path('changeRequest/list', views.listChangeRequests, name='listChangeRequests'),
    path('changeRequest/<int:changeRequestId>/accept', views.acceptChangeRequest, name='acceptChangeRequest'),
    path('changeRequest/<int:changeRequestId>/reject', views.rejectChangeRequest, name='rejectChangeRequest'),
]