from django.shortcuts import render
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if request.user.is_authenticated is False:
        return HttpResponseRedirect("login")
    else:
        return render(request, 'users/user.html')

def login_view(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context = {"message":"Invalid credentials"}
            return render(request, "users/login.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))