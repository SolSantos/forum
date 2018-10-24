from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def welcome_page(request):
    if request.user.is_authenticated:
        return render(request, "forum/welcome.html")
    else:
        return render(request, "forum/login.html")


def do_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")


def do_logout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect("/")		