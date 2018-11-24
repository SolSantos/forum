from django.contrib import admin
from .models import Course, Semester, Forum, Topic, Question, Answer, Profile

# Register your models here.
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
