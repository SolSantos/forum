from .models import Course, Forum, Question

def get_courses():
	return [course.get_tree() for course in Course.objects.all()]

def get_forums_by_type(type="S"):
	return [forum.get_tree() for forum in Forum.objects.filter(type=type)]

def get_forum(forum_id):
	return Forum.objects.get(id=forum_id).get_tree()

def get_question(question_id):
	return Question.objects.get(id=question_id).get_tree()

def add_question(author, topic_id=None, forum_id=None, description=""):
	if description == "":
		return -1

	if topic_id is None and forum_id is None:
		return -1

	question = None
	if topic_id:
		topic = Topic.objects.get(id=topic_id)
		question = Question(forum=topic.forum, topic=topic, description=description, author=author)
	elif forum_id:
		forum = Forum.objects.get(id=forum_id)
		question = Question(forum=forum, description=description, author=author)

	if question is None:
		return -2

	question.save()
	return 0