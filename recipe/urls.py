from django.urls import path
from recipe import views

app_name = 'recipe'
urlpatterns = [
    path('show/<int:recetaId>', views.showReceta, name='show'),
    path('create', views.createReceta, name='create'),

] 