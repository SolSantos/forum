from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from forum.models import Question
from forum.models import Answer
from forum.models import Forum

from forum.controller import get_questions
from forum.controller import get_filtering_state
from forum.controller import get_topics
from forum.controller import add_question
from forum.controller import add_answer
from forum.controller import upvote_answer as controller_upvote_answer
from forum.controller import downvote_answer as controller_downvote_answer
from forum.controller import cancel_vote
from forum.controller import remove_question
from forum.controller import remove_answer
from forum.controller import get_courses


@login_required
def course_welcome_page(request, filter_type=1, course_id=None, subject_id=None, search=""):
    render_state = {
        "selected_item": 1,
        "filtering_state": get_filtering_state(
            selected_menu=1,
            user=request.user,
            course_id=course_id,
            subject_id=subject_id
        )
    }

    questions = get_questions(render_state["filtering_state"], search)
    topics = get_topics()
    courses = get_courses()
    subjects = [
        forum.as_dict() for forum in Forum.objects.filter(
            semester__course__name=render_state["filtering_state"]["topic"]
        )
    ]

    return render(request, "forum/index.html", {
        "questions": questions,
        "render_state": render_state,
        "topics": topics,
        "courses": courses,
        "subjects": subjects
    })


def welcome_page(request, filter_type=0, search=""):
    if request.user.is_authenticated:
        render_state = {
            "selected_item": filter_type,
            "filtering_state": get_filtering_state(filter_type, request.user)
        }

        questions = get_questions(render_state["filtering_state"], search)
        topics = get_topics()
        courses = get_courses()

        subjects = []
        if render_state["selected_item"] == 1:
            subjects = [
                forum.as_dict() for forum in Forum.objects.filter(
                    semester__course__name=render_state["filtering_state"]["topic"]
                )
            ]

        return render(request, "forum/index.html", {
            "questions": questions,
            "render_state": render_state,
            "topics": topics,
            "courses": courses,
            "subjects": subjects
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
    answers = [
        {
            "title": answer.question.title,
            "question_id": answer.question.id,
            **answer.as_dict(author=request.user)
        }
        for answer in Answer.objects.filter(author=request.user)
    ]

    return render(request, "forum/minhas_respostas.html", {
        "answers": answers,
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
    question = Question.objects.get(id=question_id)
    answers = [answer.as_dict(author=request.user) for answer in question.answer_set.all()]
    answers = sorted(
        answers,
        key=lambda answer: answer["positive_votes"] - answer["negative_votes"],
        reverse=True
    )

    return render(request, "forum/pergunta.html", {
        "question": question.as_dict(),
        "answers": answers
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


@login_required
def answer_question(request):
    if request.POST:
        question_id = request.POST.get("question_id", "")
        description = request.POST.get("description", "")

        answer_id = add_answer(
            author=request.user,
            question_id=question_id,
            description=description
        )

        return redirect("/pergunta/" + str(question_id) + "/")
    else:
        return redirect("/")


vote_action_strategy = {
    "upvote": controller_upvote_answer,
    "downvote": controller_downvote_answer,
    "cancel": cancel_vote
}


def __apply_vote_answer_action(request, action, author, answer_id):
    vote_action_strategy[action](
        author=author,
        answer_id=answer_id
    )

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def upvote_answer(request, answer_id=None):
    return __apply_vote_answer_action(request, "upvote", request.user, answer_id)


@login_required
def downvote_answer(request, answer_id=None):
    return __apply_vote_answer_action(request, "downvote", request.user, answer_id)


@login_required
def cancel_vote_answer(request, answer_id=None):
    return __apply_vote_answer_action(request, "cancel", request.user, answer_id)


@login_required
def delete_question(request, question_id=None):
    remove_question(author=request.user, question_id=question_id)
    return redirect("/minhas_perguntas/")


@login_required
def delete_answer(request, answer_id=None):
    remove_answer(author=request.user, answer_id=answer_id)
    return redirect("/minhas_respostas/")
