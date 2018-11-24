from django.urls import path
from . import views
from . import api

urlpatterns = [
	# Views
	path('', views.welcome_page, name='welcome_page'),
	path('login/', views.do_login, name='login'),
	path('logout/', views.do_logout, name='logout'),
	path('see_courses/', views.see_courses, name='see_courses'),

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
