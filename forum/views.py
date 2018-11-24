from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from forum.models import Question


def welcome_page(request):
    if request.user.is_authenticated:
        questions = [
            {
                "topic": "Licenciatura em Design e Multimédia",
                "subtopic": "Sistemas Informáticos",
                "title": "SQL - Como selecionar elementos de uma tabela que obedeçam uma certa condição?",
                "description": "Por exemplo, se eu tiver uma tabela de empregados e quiser selecionar os que têm salário maior que 1000€, como faço?"
            },
            {
                "topic": "SASUC",
                "title": "Como me posso candidatar a bolsa de estudo?"
            },
            {
                "topic": "DEI",
                "title": "Onde fica a helpdesk?"
            },
            {
                "topic": "SASUC",
                "title": "Quando sai o resultado da minha candidatura à bolsa de estudo?",
                "description": "Sei que algumas pessoas já souberam do resultado, outras dizem que demora imensos meses. Afinal quando é que eu devo saber?"
            }
        ]
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
