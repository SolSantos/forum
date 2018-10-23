from django.urls import path
from . import views
from . import api

urlpatterns = [
	path('', views.welcome_page, name='welcome_page'),
	path('get_courses/', api.get_courses, name='get_courses'),
	path('get_regular_forums/', api.get_regular_forums, name='get_regular_forums'),
	path('get_other_forums/', api.get_other_forums, name='get_other_forums'),
	path('get_forum/<int:forum_id>/', api.get_forum, name='get_forum'),
	path('get_question/<int:question_id>/', api.get_question, name='get_question')
]
