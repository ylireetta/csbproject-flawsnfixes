from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

def index(request):
    # not working atm - the form is not included for some reason
    return render(request, 'registration/login.html')