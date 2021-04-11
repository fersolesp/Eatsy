from django.urls import path
from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('signup', views.signUp, name='signUp'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.myProfile, name='profile'),
] 