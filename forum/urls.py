from django.urls import path
from . import views

urlpatterns = [
	# Views
	path('', views.welcome_page, name='welcome_page'),
	path('<int:filter_type>/', views.welcome_page, name='welcome_page'),
	path('<int:filter_type>/<int:course_id>/', views.course_welcome_page, name='course_welcome_page'),
	path('<int:filter_type>/<int:course_id>/<int:subject_id>/', views.course_welcome_page, name='course_welcome_page'),
	path('<int:filter_type>/<str:search>/', views.welcome_page, name='welcome_page'),
	path('login/', views.do_login, name='login'),
	path('logout/', views.do_logout, name='logout'),
	path('minhas_perguntas/', views.my_questions_page, name='my_questions_page'),
	path('minhas_respostas/', views.my_answers_page, name='my_answers_page'),
	path('pergunta/<int:question_id>/', views.question_page, name='question_page'),
	path('create_question/', views.create_question, name='create_question'),
	path('answer_question/', views.answer_question, name='answer_question'),
	path('upvote/<int:answer_id>/', views.upvote_answer, name='upvote_answer'),
	path('downvote/<int:answer_id>/', views.downvote_answer, name='downvote_answer'),
	path('cancelvote/<int:answer_id>/', views.cancel_vote_answer, name='cancel_vote_answer'),
	path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
	path('delete_answer/<int:answer_id>/', views.delete_answer, name='delete_answer')
]
