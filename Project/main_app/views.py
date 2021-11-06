from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Profile


def Home(request):
    return render(request, 'main_app/home.html')


def About_Us(request):
    return render(request, 'main_app/about.html')


@login_required(login_url='login')
def User_Profile(request):
    user = Profile.objects.get(user__username=request.user.username)
    name = user.fullName
    return render(request, 'main_app/profile.html', {'name':name})
