from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from main_app.models import Profile
from .CredentialChecker import passwordCheck, usernameCheck

def user_login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    else:
        if request.POST['username'] and request.POST['password']:
            try:
                # user = User.objects.get(email=request.POST['email'])
                user = User.objects.get(username=request.POST['username'])
                user = auth.authenticate(username=user.username, password=request.POST['password'])

                if user is not None:
                    auth.login(request, user)
                    return redirect('home')

                else:
                    return render(request, 'accounts/login.html', {'error': 'Username/Email and Password do not match'})

            except User.DoesNotExist:
                return render(request, 'accounts/login.html', {'error': 'User is not registered'})

        else:
            return render(request, 'accounts/login.html', {'error': 'Username or Password cannot be empty!'})

def user_registration(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')

    else:
        if request.POST['email'] and request.POST['username'] and request.POST['fullname'] and request.POST['pass1'] and request.POST['pass2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username already exists'})

            except User.DoesNotExist:
                try:
                    User.objects.get(email=request.POST['email'])
                    return render(request, 'accounts/signup.html', {'error': 'Email already exists'})

                except User.DoesNotExist:
                    if request.POST['pass1'] == request.POST['pass2']:
                        ck = usernameCheck(request.POST['username'])
                        if ck!=1:
                            if ck == 2:
                                return render(request, 'accounts/signup.html', {'error': 'Username must be 4-15 characters long.'})
                            else:
                                return render(request, 'accounts/signup.html', {'error': 'Username can contain only letters, digits and under_scores'})

                        ck = passwordCheck(request.POST['pass1'])
                        if ck != 1:
                            if ck == 2:
                                return render(request, 'accounts/signup.html',
                                              {'error': 'Password must be 6-30 characters long.'})
                            else:
                                return render(request, 'accounts/signup.html',
                                              {'error': 'Password must contain both letters and digits'})

                        user = User.objects.create_user(username=request.POST['username'], password=request.POST['pass1'], email=request.POST['email'])
                        auth.login(request, user)
                        fullname = request.POST['fullname']
                        profile = Profile(user=user, fullName=fullname)
                        profile.save()

                        return redirect('home')

                    else:
                        return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})


        else:
            return render(request, 'accounts/signup.html', {'error':'Please Fill Up all the Information'})


@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    return redirect('home')