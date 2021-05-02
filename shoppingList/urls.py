from django.urls import path

from shoppingList import views

app_name = 'shoppingList'
urlpatterns = [
    path('', views.show, name='show'),
    path('remove/<int:productId>', views.removeProduct, name='removeProduct'),
    path('empty', views.empty, name='empty'),
]
