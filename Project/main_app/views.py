from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import auth
from django.conf import settings
from django.core.mail import send_mail
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Profile, Tutorial, Reading_list, Topic_Recommendation
from . import Recommendation


def Home(request):
    tut_obj = Tutorial.objects.filter(isApproved=True).order_by('-id')

    paginator = Paginator(tut_obj, 10)
    page_num = request.GET.get('page', 1)

    try:
        details = paginator.page(page_num)
    except PageNotAnInteger:
        details = paginator.page(1)
    except EmptyPage:
        details = paginator.page(paginator.num_pages)

    return render(request, 'main_app/home.html', {'tutorials': details})


def About_Us(request):
    return render(request, 'main_app/about.html')


def Contact_Us(request):
    if request.method == 'GET':
        return render(request, 'main_app/contactus.html')

    else:
        subject = 'AlgoVault message'
        message = f"Name: {request.POST['name']}\nEmail: {request.POST['email']}\nSubject: {request.POST['subject']}\n\n{request.POST['message']}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['nsakib800@gmail.com']
        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'main_app/contactus.html', {'msg': 'msg'})


def tutorial_list(request):
    tut_obj = Tutorial.objects.filter(isApproved=True).order_by('level')
    tut_dict = {}

    for tut in tut_obj:
        tut_dict[tut.tag] = []

    for tut in tut_obj:
        tut_dict[tut.tag].append(tut)

    return render(request, 'main_app/tutoriallist.html', {'tutorials': tut_dict})


def tutorial_details(request, tut_id):
    tut_obj = Tutorial.objects.filter(id=tut_id).first()
    done = False

    try:
        read = Reading_list.objects.filter(user=request.user, article__id=tut_id).first()
        if read is not None:
            done = True
    except:
        pass

    return render(request, 'main_app/tutorialdetails.html', {'tutorial': tut_obj, 'read': done})


@login_required(login_url='login')
def mark_as_done(request, tut_id):
    article = Tutorial.objects.filter(id=tut_id).first()
    Reading_list.objects.create(user=request.user, article=article)
    try:
        suggest = Topic_Recommendation.objects.filter(user=request.user).first()
    except:
        Topic_Recommendation.objects.create(user=request.user, topic1=' ', topic2=' ')
        suggest = Topic_Recommendation.objects.filter(user=request.user).first()

    rec = Recommendation.recommender(request)

    suggest.topic1 = rec[0]
    suggest.topic2 = rec[1]

    suggest.save()

    return redirect('tutDetails', tut_id)


@login_required(login_url='login')
def User_Profile(request):
    user = Profile.objects.get(user__username=request.user.username)
    name = user.fullName
    return render(request, 'main_app/profile.html', {'name': name})


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
                return render(request, 'main_app/profile.html', {'error': 'Incorrect Password'})


        except:
            return render(request, 'main_app/profile.html', {'error': 'Incorrect Password'})



    except:
        return render(request, 'main_app/profile.html', {'error': 'Invalid Password'})


@login_required(login_url='login')
def approved_posts(request):
    tut_obj = Tutorial.objects.filter(author=request.user, isApproved=True).order_by('-id')

    paginator = Paginator(tut_obj, 10)
    page_num = request.GET.get('page', 1)

    try:
        details = paginator.page(page_num)
    except PageNotAnInteger:
        details = paginator.page(1)
    except EmptyPage:
        details = paginator.page(paginator.num_pages)

    return render(request, 'main_app/approvedposts.html', {'tutorials': details})


@login_required(login_url='login')
def pending_posts(request):
    tut_obj = Tutorial.objects.filter(author=request.user, isApproved=False).order_by('-id')

    paginator = Paginator(tut_obj, 10)
    page_num = request.GET.get('page', 1)

    try:
        details = paginator.page(page_num)
    except PageNotAnInteger:
        details = paginator.page(1)
    except EmptyPage:
        details = paginator.page(paginator.num_pages)

    return render(request, 'main_app/pendingposts.html', {'tutorials': details})


@login_required(login_url='login')
def review_posts(request):
    if request.user.is_staff or request.user.is_superuser:
        tut_obj = Tutorial.objects.exclude(author=request.user).filter(isApproved=False)

        paginator = Paginator(tut_obj, 10)
        page_num = request.GET.get('page', 1)

        try:
            details = paginator.page(page_num)
        except PageNotAnInteger:
            details = paginator.page(1)
        except EmptyPage:
            details = paginator.page(paginator.num_pages)

        return render(request, 'main_app/reviewposts.html', {'tutorials': details})

    else:
        return redirect('home')


@login_required(login_url='login')
def approve_post(request, post_id):
    tut_obj = Tutorial.objects.filter(id=post_id).first()
    tut_obj.isApproved = True
    tut_obj.save()

    return redirect('reviewposts')


@login_required(login_url='login')
def edit_post(request, post_id):
    tut_obj = Tutorial.objects.filter(id=post_id).first()

    if request.method == 'GET':
        form = PostForm(instance=tut_obj)
        return render(request, 'main_app/editTutorial.html', {'form': form})

    else:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            tut_obj.title = form.title
            tut_obj.level = form.level
            tut_obj.tag = form.tag
            tut_obj.content = form.content
            tut_obj.save()
        return redirect('viewpost', post_id)


@login_required(login_url='login')
def add_tutorial(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'main_app/addtutorial.html', {'form': form})

    else:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
        return redirect('pendingposts')


@login_required(login_url='login')
def view_post(request, post_id):
    tut_obj = Tutorial.objects.filter(id=post_id).first()
    return render(request, 'main_app/viewPost.html', {'tutorial': tut_obj})


@login_required(login_url='login')
def progress_view(request):
    tut_obj = Reading_list.objects.filter(user=request.user)

    qs = {}

    for tut in tut_obj:
        try:
            qs[tut.article.tag] += 1
        except:
            qs[tut.article.tag] = 1

    for key, val in qs.items():
        qs[key] = (val * 100) / Tutorial.objects.filter(tag=key).count()
        qs[key] = round(qs[key], 2)

    try:
        rec = Topic_Recommendation.objects.filter(user=request.user).first()
        suggestion = [rec.topic1, rec.topic2]
        if suggestion[0] is None or suggestion[1] is None:
            suggestion = Recommendation.recommender(request)
            rec.topic1 = suggestion[0]
            rec.topic2 = suggestion[1]
            rec.save()

    except:
        suggestion = Recommendation.recommender(request)
        Topic_Recommendation.objects.create(user=request.user, topic1=suggestion[0])

    data = []

    if suggestion[0] is not None:
        id = Recommendation.getID(suggestion[0])
        data.append((suggestion[0], id))
    else:
        data.append((suggestion[0], -1))

    if suggestion[1] is not None:
        id = Recommendation.getID(suggestion[1])
        data.append((suggestion[1], id))
    else:
        data.append((suggestion[1], -1))


    return render(request, 'main_app/progress.html', {'qs': qs, 'suggestions':data})
