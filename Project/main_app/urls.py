from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About_Us, name='aboutUs'),
    path('profile', views.User_Profile, name='profile'),
    path('updateprofile', views.Update_Profile, name='updateprofile'),
    path('contact', views.Contact_Us, name='contactUs'),
    path('tutorials', views.tutorial_list, name='tutorials'),
    path('details', views.tutorial_details, name='tutDetails'),
]