from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from forum.models import Question
from forum.controller import get_questions
from forum.controller import get_filtering_state


def welcome_page(request, filter_type=0, search=""):
    if request.user.is_authenticated:
        render_state = {
            "selected_item": filter_type,
            "filtering_state": get_filtering_state(filter_type, request.user)
        }

        questions = get_questions(render_state["filtering_state"], search)
        return render(request, "forum/index.html", {
            "questions": questions,
            "render_state": render_state
        })
    else:
        return render(request, "forum/login.html")


def my_questions_page(request):
    questions = [question.as_dict() for question in Question.objects.filter(author=request.user)]
    return render(request, "forum/minhas_perguntas.html", {
        "questions": questions,
    })


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
