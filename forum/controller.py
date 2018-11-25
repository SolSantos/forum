from .models import Course
from .models import Forum
from .models import Question
from .models import Topic
from .models import Answer
from .models import Profile
from django.db.models import Q


def get_topics():
	topics = []
	for forum in Forum.objects.filter(type="S"):
		course_description = forum.semester.course.name
		if forum.semester.course.short_name:
			course_description = forum.semester.course.short_name

		topics.append({
			"id": forum.id,
			"type": forum.type,
			"description": course_description + " - " + forum.name
		})

	for topic in Topic.objects.filter(forum__type="O"):
		topics.append({
			"id": topic.id,
			"type": topic.forum.type,
			"description": topic.forum.name + " - " + topic.name
		})

	return topics

filter_by_selected_menu = {
	0: None,
	1: {
		"option": "S",
		"topic": "Licenciatura em Engenharia Informática",
		"subtopic": ""
	},
	2: {
		"option": "O",
		"topic": "SASUC",
		"subtopic": ""
	},
	3: {
		"option": "O",
		"topic": "DEI",
		"subtopic": ""
	},
	4: {
		"option": "O",
		"topic": "Praxe",
		"subtopic": ""
	},
	5: {
		"option": "O",
		"topic": "Erasmus",
		"subtopic": ""
	},
	6: {
		"option": "O",
		"topic": "AAC",
		"subtopic": ""
	}
}


def get_filtering_state(selected_menu, user=None):
	filtering_state = filter_by_selected_menu[selected_menu]
	if selected_menu == 1:
		try:
			filtering_state["topic"] = Profile.objects.get(user=user).course.name
		except Profile.DoesNotExist:
			pass
	return filtering_state


def get_courses():
	return [course.get_tree() for course in Course.objects.all()]


def get_forums_by_type(type="S"):
	return [forum.get_tree() for forum in Forum.objects.filter(type=type)]


def get_forum(forum_id):
	return Forum.objects.get(id=forum_id).get_tree()


def get_question(question_id):
	return Question.objects.get(id=question_id).get_tree()


def get_questions(filtering_state=None, search=""):
	questions = []

	if filtering_state:
		if filtering_state["option"] and filtering_state["option"] != "":
			if filtering_state["option"] == "O":
				questions = Question.objects.filter(
					forum__type=filtering_state["option"],
					topic__name=filtering_state["topic"]
				)
			elif filtering_state["option"] == "S":
				questions = Question.objects.filter(
					forum__type=filtering_state["option"],
					forum__semester__course__name=filtering_state["topic"]
				)
	else:
		questions = Question.objects.all()

	if search and search != "":
		keywords = search.strip("?!.;").split(" ")
		set_questions = set()
		for word in keywords:
			set_questions |= set(questions.filter(
				Q(title__icontains=word) |
				Q(description__icontains=word)
			))

		questions = set_questions

	# get all questions
	return [question.as_dict() for question in questions]


def add_question(author, topic_id=None, forum_id=None, description="", title=""):
	if topic_id is None and forum_id is None:
		return -1

	question = None
	if topic_id:
		try:
			topic = Topic.objects.get(id=topic_id)
		except Topic.DoesNotExist as e:
			return -2

		question = Question(forum=topic.forum, topic=topic, description=description, author=author, title=title)
	elif forum_id:
		try:
			forum = Forum.objects.get(id=forum_id)
		except Forum.DoesNotExist as e:
			return -2

		question = Question(forum=forum, description=description, author=author, title=title)

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
	if question_id is None:
		return -1

	if description == "":
		return -1

	try:
		question = Question.objects.get(id=question_id)
	except Question.DoesNotExist as e:
		return -2

	answer = Answer(author=author, question=question, description=description)
	answer.full_clean()
	answer.save()
	return answer.id


def edit_answer(author, answer_id=None, description=""):
	if answer_id is None:
		return -1

	if description == "":
		return -1

	try:
		answer = Answer.objects.get(id=answer_id)
	except Answer.DoesNotExist as e:
		return -2

	if author != answer.author:
		return -3

	answer.description = description
	answer.save()
	return 0


def remove_answer(author, answer_id=None):
	if answer_id is None:
		return -1

	try:
		answer = Answer.objects.get(id=answer_id)
	except Answer.DoesNotExist as e:
		return -2

	if answer.author != author:
		return -3

	answer.delete()
	return 0



def cancel_vote(author, answer_id=None):
	if answer_id is None:
		return -1

	try:
		answer = Answer.objects.get(id=answer_id)
	except Answer.DoesNotExist as e:
		return -2

	if author in answer.positive_votes.all():
		answer.positive_votes.remove(author)

	if author in answer.negative_votes.all():
		answer.negative_votes.remove(author)

	return 0


def upvote_answer(author, answer_id=None):
	if answer_id is None:
		return -1

	try:
		answer = Answer.objects.get(id=answer_id)
	except Answer.DoesNotExist as e:
		return -2

	cancel_vote(author, answer_id)
	answer.positive_votes.add(author)
	answer.save()
	return 0


def downvote_answer(author, answer_id=None):
	if answer_id is None:
		return -1

	try:
		answer = Answer.objects.get(id=answer_id)
	except Answer.DoesNotExist as e:
		return -2

	cancel_vote(author, answer_id)
	answer.negative_votes.add(author)
	answer.save()
	return 0
