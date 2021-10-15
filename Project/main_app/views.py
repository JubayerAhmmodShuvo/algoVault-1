from django.shortcuts import render

def Home(request):
    return render(request, 'main_app/home.html')
