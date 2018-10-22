from django.core.management.base import BaseCommand
from forum_uc.settings import BASE_DIR
from forum.models import Course, Semester, Forum, Topic
import json
import datetime

INITIAL_DATA_FILE = BASE_DIR + "/forum/initial_forum_data.json"


class Command(BaseCommand):
    help = 'Import initial wanted data for the forums'

    def handle(self, *args, **options):
        initial_data = None

        with open(INITIAL_DATA_FILE, "r") as data_file:
            initial_data = json.loads(data_file.read())

        if not initial_data:
            self.stdout.write(self.style.ERROR(
                "Failed to load the data from the json file")
            )

        course_forums = initial_data["course_forums"]
        other_forums = initial_data["other_forums"]

        # Create the course forums and all the associated course tree
        for course in course_forums:
            course_instance = Course.objects.create(
                name=course["course"],
                created_at=datetime.datetime.now()
            )

            for semester in course["semesters"]:
                semester_instance = Semester.objects.create(
                    course=course_instance,
                    year=semester["year"],
                    semester=semester["semester"],
                    created_at=datetime.datetime.now()
                )

                for subject in semester["subjects"]:
                    Forum.objects.create(
                        semester=semester_instance,
                        name=subject,
                        type="S",
                        created_at=datetime.datetime.now()
                    )

        # Create the other forums and the associated topics
        for forum in other_forums:
            forum_instance = Forum.objects.create(
                name=forum["name"],
                type="O",
                created_at=datetime.datetime.now()
            )

            for topic in forum["topics"]:
                Topic.objects.create(
                    forum=forum_instance,
                    name=topic,
                    created_at=datetime.datetime.now()
                )
