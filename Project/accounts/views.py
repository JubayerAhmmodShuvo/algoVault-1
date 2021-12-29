import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from main_app.models import Profile
from .CredentialChecker import passwordCheck, usernameCheck
from django.conf import settings
from django.core.mail import send_mail

def user_login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    else:
        if request.POST['username'] and request.POST['password']:
            try:
                user = User.objects.get(username=request.POST['username'])
                user = auth.authenticate(username=user.username, password=request.POST['password'])

                if user is not None:
                    profile_obj = Profile.objects.get(user__username=user.username)
                    if profile_obj.isVarified == False:
                        return render(request, 'accounts/login.html', {'error': 'Account is not verified'})

                    auth.login(request, user)
                    return redirect('home')

                else:
                    return render(request, 'accounts/login.html', {'error': 'Username and Password do not match'})

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
                        fullname = request.POST['fullname']
                        token = str(uuid.uuid4())
                        profile = Profile(user=user, fullName=fullname, auth_token=token, email=request.POST['email'])
                        profile.save()

                        send_email_for_verification(request.POST['email'], token)
                        return redirect('emailsent')

                    else:
                        return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})


        else:
            return render(request, 'accounts/signup.html', {'error':'Please Fill Up all the Information'})


@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    return redirect('home')



def reset_password(request):
    if request.method == 'GET':
        return render(request, 'accounts/recoverpassword.html')

    else:
        try:
            profile_obj = Profile.objects.filter(email=request.POST['email']).first()
            token = str(uuid.uuid4())
            profile_obj.auth_token = token

            profile_obj.save()
            send_email_for_reset_password(request.POST['email'], token)

            return redirect('emailsent')

        except:
            return render(request, 'accounts/recoverpassword.html', {'error':'Invalid email address'})



def send_email_for_verification(email, token):
    subject = "User Verification for AlgoVault"
    message = f'Thank you for registering.\nPlease click the link for verification: http://127.0.0.1:8000/accounts/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



def send_email_for_reset_password(email, token):
    subject = "Password Reset for AlgoVault"
    message = f'Click the link below to reset your password.\nhttp://127.0.0.1:8000/accounts/reset/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



def email_sent(request):
    return render(request, 'accounts/emailSent.html')



def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.isVarified:
                return render(request, 'accounts/login.html', {'success_msg':'Account already verified'})

            profile_obj.isVarified = True
            profile_obj.auth_token = 'n'
            profile_obj.save()

            return render(request, 'accounts/login.html', {'success_msg':'Account has been verified'})

    except Exception as e:
        print(e)



def verify_new_password_token(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        username = User.objects.get(email=profile_obj.email).username
        if profile_obj:
            return render(request, 'accounts/confirmresetpass.html', {'username':username})

    except Exception as e:
        print(e)



def set_new_password(request, username):
    try:
        user = User.objects.get(username=username)

        if(request.POST['password1'] == request.POST['password2']):
            profile_obj = Profile.objects.get(email=user.email)
            profile_obj.auth_token = 'n'
            user.set_password(request.POST['password1'])
            user.save()
            profile_obj.save()
            return redirect('login')

        else:
            return render(request, 'accounts/confirmresetpass.html', {'error':'passwords do not match'})


    except Exception as e:
        print(e)