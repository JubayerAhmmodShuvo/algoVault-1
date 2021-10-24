from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About_Us, name='aboutUs'),
    path('profile', views.User_Profile, name='profile'),
]