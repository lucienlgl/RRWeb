from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("rrsite app index")


def login(request):
    return render(request, 'rrsite/login.html')


def register(request):
    return render(request, 'rrsite/register.html')
