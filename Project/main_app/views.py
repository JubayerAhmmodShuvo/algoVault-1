from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth

from .models import Profile


def Home(request):
    return render(request, 'main_app/home.html')


def About_Us(request):
    return render(request, 'main_app/about.html')


def Contact_Us(request):
    return render(request, 'main_app/contactus.html')


def tutorial_list(request):
    return render(request, 'main_app/tutoriallist.html')


def tutorial_details(request):
    return render(request, 'main_app/tutorialdetails.html')


@login_required(login_url='login')
def User_Profile(request):
    user = Profile.objects.get(user__username=request.user.username)
    name = user.fullName
    return render(request, 'main_app/profile.html', {'name':name})


@login_required(login_url='login')
def Update_Profile(request):
    profile_obj = Profile.objects.get(user__username=request.user.username)

    try:
        password = request.POST['current_password']

        try:
            user = auth.authenticate(username=request.user.username, password=password)

            if user is not None:
                user = User.objects.get(username=request.user.username)

                try:
                    profile_obj.fullName = request.POST['fullname']
                except:
                    pass

                try:
                    profile_obj.email = request.POST['email']
                    user.email = request.POST['email']
                except:
                    pass

                try:
                    if request.POST['new_password'] == request.POST['new_password2'] and request.POST['new_password']:
                        user.set_password(request.POST['new_password'])
                except:
                    pass

                user.save()
                profile_obj.save()

                return redirect('profile')

            else:
                return render(request, 'main_app/profile.html', {'error':'Incorrect Password'})


        except:
            return render(request, 'main_app/profile.html', {'error':'Incorrect Password'})



    except:
        return render(request, 'main_app/profile.html', {'error':'Invalid Password'})
