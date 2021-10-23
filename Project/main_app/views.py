from django.shortcuts import render

def Home(request):
    return render(request, 'main_app/home.html')

def About_Us(request):
    return render(request, 'main_app/about.html')
