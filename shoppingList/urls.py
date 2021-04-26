from django.urls import include, path

from shoppingList import views

app_name = 'shoppingList'
urlpatterns = [
    path('', views.show, name='show'),
    path('empty', views.empty, name='empty'),
] 
