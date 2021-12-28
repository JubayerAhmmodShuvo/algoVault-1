from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('signup', views.user_registration, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('emailsent', views.email_sent, name='emailsent'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('resetpass', views.reset_password, name='reset_password'),
    path('reset/<auth_token>', views.verify_new_password_token, name='reset_verify'),
    path('newpass/<username>', views.set_new_password, name='new_password')
]