from django.urls import path
from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('signup', views.signUp, name='signUp'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create-subscription', views.createSubscription, name='createSuscription'),
    path('create-customer', views.create_customer, name='createCustomer'),
    path('profile', views.myProfile, name='profile')
] 