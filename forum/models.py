from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from forum.helpers import get_date_for_display
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Course(models.Model):
    name = models.CharField(unique=True, max_length=200)
    short_name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_tree(self):
        semesters = []

        for semester in self.semester_set.all():
            current_semester = semester.as_dict()

            forums = []
            for forum in semester.forum_set.all():
                forums.append(forum.as_dict())

            current_semester["forums"] = forums
            semesters.append(current_semester)

        return {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "semesters": semesters
        }


class Profile(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.DO_NOTHING)


@receiver(post_save, sender=User)
def register_user_profile(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)


class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.course) + " " + str(self.year) + "º year, " + str(self.semester) + "º semester"

    def as_dict(self):
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

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "type_label": self.get_type_display(),
            "created_at": str(self.created_at)
        }

    def get_tree(self):
        forum_tree = self.as_dict()

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

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at)
        }

    def get_tree(self):
        topic_tree = self.as_dict()
        topic_tree["questions"] = [question.get_tree() for question in self.question_set.all()]
        return topic_tree


class Question(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=600, default="", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def as_dict(self):
        question_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author.get_full_name(),
            "created_at": self.created_at,
            "date_for_display": get_date_for_display(self.created_at)
        }

        if self.forum.type == "S":
            question_dict["topic"] = self.forum.semester.course.name
            question_dict["subtopic"] = self.forum.name
        else:
            question_dict["topic"] = self.topic.name

        return question_dict

    def get_tree(self):
        question_tree = self.as_dict()
        question_tree["answers"] = [answer.as_dict() for answer in self.answer_set.all()]
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

    def as_dict(self, author=None):
        answer_dict = {
            "id": self.id,
            "description": self.description,
            "author": self.author.get_full_name(),
            "created_at": get_date_for_display(self.created_at),
            "positive_votes": self.positive_votes.all().count(),
            "negative_votes": self.negative_votes.all().count(),
        }

        if author:
            answer_dict["author_in_positive_votes"] = author in self.positive_votes.all()
            answer_dict["author_in_negative_votes"] = author in self.negative_votes.all()

        return answer_dict
