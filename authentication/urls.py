from django.urls import path
from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('signUp', views.signUp, name='signUp'),
] 