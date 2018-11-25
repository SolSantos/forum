from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from forum.models import Question
from forum.controller import get_questions
from forum.controller import get_filtering_state

from forum.controller import get_topics
from forum.controller import add_question

from forum.models import Forum
from forum.models import Topic


def welcome_page(request, filter_type=0, search=""):
    if request.user.is_authenticated:
        render_state = {
            "selected_item": filter_type,
            "filtering_state": get_filtering_state(filter_type, request.user)
        }

        questions = get_questions(render_state["filtering_state"], search)
        topics = get_topics()
        return render(request, "forum/index.html", {
            "questions": questions,
            "render_state": render_state,
            "topics": topics
        })
    else:
        return render(request, "forum/login.html")


@login_required
def my_questions_page(request):
    questions = [question.as_dict() for question in Question.objects.filter(author=request.user)]
    return render(request, "forum/minhas_perguntas.html", {
        "questions": questions,
    })

@login_required
def my_answers_page(request):
    questions = [question.as_dict() for question in Question.objects.filter(author=request.user)]
    return render(request, "forum/minhas_respostas.html", {
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


def question_page(request, question_id):
    question = Question.objects.get(id=question_id).as_dict()
    return render(request, "forum/pergunta.html", {
        "question": question,
    })


@login_required
def create_question(request):
    if request.POST:
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        topic = request.POST.get("topic")

        topic_tokens = topic.split("|")
        forum_id = None 
        topic_id = None
        if topic_tokens[1] == "S":
            forum_id = topic_tokens[0]
        elif topic_tokens[1] == "O":
            topic_id = topic_tokens[0]

        question_id = add_question(
            author=request.user,
            topic_id=topic_id,
            forum_id=forum_id,
            description=description,
            title=title
        )

        return redirect("/pergunta/" + str(question_id) + "/")
    else:
        return redirect("/")

