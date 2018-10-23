from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Course(models.Model):
	name = models.CharField(unique=True, max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def get_tree(self):
		semesters = []

		for semester in self.semester_set.all():
			current_semester = semester.as_json()

			forums = []
			for forum in semester.forum_set.all():
				forums.append(forum.as_json())

			current_semester["forums"] = forums
			semesters.append(current_semester)

		return {
			"id": self.id,
			"name": self.name,
			"created_at": str(self.created_at),
			"semesters": semesters
		}


class Semester(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	year = models.IntegerField()
	semester = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)	

	def __str__(self):
		return str(self.course) + " " + str(self.year) + "º year, " + str(self.semester) + "º semester"

	def as_json(self):
		return {
			"id": self.id,
			"year": self.year,
			"semester": self.semester,
			"created_at": str(self.created_at)
		}


class Forum(models.Model):
	type_choices = (
		("S", "Subject"),
		("O", "Other")
	)

	semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200)
	type = models.CharField(choices=type_choices, default="S", max_length=1)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


	def as_json(self):
		return {
			"id": self.id,
			"name": self.name,
			"type": self.type,
			"type_label": self.get_type_display(),
			"created_at": str(self.created_at)
		}

	def get_tree(self):
		forum_tree = self.as_json()
		
		if self.type == "O":
			forum_tree["topics"] = [topic.get_tree() for topic in self.topic_set.all()]
		else:
			forum_tree["questions"] = [question.get_tree() for question in self.question_set.all()]

		return forum_tree


class Topic(models.Model):
	forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return {
			"id": self.id,
			"name": self.name,
			"created_at": str(self.created_at)
		}

	def get_tree(self):
		topic_tree = self.as_json()
		topic_tree["questions"] = [question.get_tree() for question in self.question_set.all()]
		return topic_tree


class Question(models.Model):
	forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
	description = models.CharField(max_length=600)
	author = models.ForeignKey(User, on_delete=models.PROTECT)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def as_json(self):
		return {
			"id": self.id,
			"description": self.description,
			"author": self.author.username,
			"created_at": str(self.created_at)
		}

	def get_tree(self):
		question_tree = self.as_json()
		question_tree["answers"] = [answer.as_json() for answer in self.answer_set.all()]
		return question_tree

	def save(self, *args, **kwargs):
		if self.forum.type == "S" and self.topic:
			raise ValidationError("""Cannot set a 'Subject' forum and the topic at the same time in
		 	the question.""")

		self.full_clean()
		super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	description = models.CharField(max_length=1200)
	positive_votes = models.ManyToManyField(User, related_name="positive_votes")
	negative_votes = models.ManyToManyField(User, related_name="negative_votes")
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="author")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.description

	def as_json(self):
		return {
			"id": self.id,
			"description": self.description,
			"author": self.author.username,
			"created_at": str(self.created_at),
			"votes": self.positive_votes.all().count() - self.negative_votes.all().count()
		}