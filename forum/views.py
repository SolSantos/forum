from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from forum.models import Question


def welcome_page(request):
    if request.user.is_authenticated:
        questions = [question.as_dict() for question in Question.objects.all()]
        return render(request, "forum/index.html", {"questions": questions})
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


def see_courses(request):
    question = Question.objects.all()
    return render(request, "forum/see_courses.html", {"questions": question})
