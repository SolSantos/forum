from .models import Course, Forum, Question, Topic

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
		try:
			topic = Topic.objects.get(id=topic_id)
		except Topic.DoesNotExist as e:
			return -2

		question = Question(forum=topic.forum, topic=topic, description=description, author=author)
	elif forum_id:
		try:
			forum = Forum.objects.get(id=forum_id)
		except Forum.DoesNotExist as e:
			return -2

		question = Question(forum=forum, description=description, author=author)

	if question is None:
		return -3

	question.save()
	return question.id

def remove_question(author, question_id=None):
	if question_id is None:
		return -1

	try:
		question = Question.objects.get(id=question_id)
	except Question.DoesNotExist as e:
		return -2

	if question.author != author:
		return -3

	question.delete()
	return 0


def add_answer(author, question_id=None, description=""):
	return 0

def edit_answer(author, question_id=None, answer_id=None, description=""):
	return 0

def remove_answer(author, question_id=None, answer_id=None):
	return 0

def upvote_answer(author, answer_id=None):
	return 0

def downvote_answer(author, answer_id=None):
	return 0

def cancel_vote(author, answer_id=None):
	return 0