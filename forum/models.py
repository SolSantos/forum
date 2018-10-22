from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
	name = models.CharField(unique=True, max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Semester(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	year = models.IntegerField()
	semester = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)	

	def __str__(self):
		return str(self.course) + " " + str(self.year)


class Forum(models.Model):
	type_choices = (
		("S", "Subject"),
		("O", "Other")
	)

	semestre = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
	name = models.CharField(unique=True, max_length=200)
	type = models.CharField(choices=type_choices, default="S", max_length=1)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Topic(models.Model):
	forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Question(models.Model):
	forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
	description = models.CharField(max_length=600)
	author = models.ForeignKey(User, on_delete=models.PROTECT)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	description = models.CharField(max_length=1200)
	votes = models.ManyToManyField(User, related_name="votes")
	author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="author")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.description