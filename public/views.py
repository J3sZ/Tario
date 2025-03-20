from django.shortcuts import render

# Create your views here.

def welcome_tario(request):
    return render(request, 'welcome_tario.html')
