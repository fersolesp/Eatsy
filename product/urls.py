from django.urls import path, include
from product import views

app_name = 'product'
urlpatterns = [
    path('show/<int:productId>', views.showProduct, name='show'),
    path('list', views.listProduct, name='list'),
    path('create', views.createProduct, name='create'),
    path('report/list', views.listReports, name='reportList'),
    path('review/<int:productId>', views.reviewProduct, name='review'),
    path('remove/<int:commentId>', views.removeComment, name='remove'),
    path('show/<int:productId>/rate', views.rateProduct, name='rate'),
    path('report/action/<int:reporteId>', views.reviewReport, name='review'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('privacyPolicy/', views.privacyPolicy, name='privacyPolicy'),
    path('show/shoppingList/add', views.addProductToShoppingList, name='addToShoppingList'),
] 