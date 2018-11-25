from django.urls import path
from . import views
from . import api

urlpatterns = [
	# Views
	path('', views.welcome_page, name='welcome_page'),
	path('<int:filter_type>/', views.welcome_page, name='welcome_page'),
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
	path('delete_answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),

	# Api
	path('get_courses/', api.get_courses, name='get_courses'),
	path('get_regular_forums/', api.get_regular_forums, name='get_regular_forums'),
	path('get_other_forums/', api.get_other_forums, name='get_other_forums'),
	path('get_forum/<int:forum_id>/', api.get_forum, name='get_forum'),
	path('get_question/<int:question_id>/', api.get_question, name='get_question'),
	path('add_question/', api.add_question, name='add_question'),
	path('remove_question/', api.remove_question, name='remove_question'),
	path('add_answer/', api.add_answer, name='add_answer'),
	path('edit_answer/', api.edit_answer, name='edit_answer'),
	path('remove_answer/', api.remove_answer, name='remove_answer')
]
