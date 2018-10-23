from django.test import TestCase
from . import controller
from django.contrib.auth.models import User
from .models import Question
from .models import Answer

# Create your tests here.

class QuestionsTestCase(TestCase):
	fixtures = ['forum/fixtures/forum/test_db.json']

	def setUp(self):
		self.user = User.objects.get(username="drmargarido")
		self.question = Question.objects.get(id=1)

	def test_add_subject_question(self):
		result = controller.add_question(self.user, None, 4, "Added new question to the db!")
		self.assertTrue(result >= 0)
		question = Question.objects.get(id=result)
		self.assertEqual(question.topic, None)
		self.assertEqual(question.forum.id, 4)

	def test_add_other_question(self):
		result = controller.add_question(self.user, 2, None, "Added new question to the db!")
		self.assertTrue(result >= 0)
		question = Question.objects.get(id=result)
		self.assertEqual(question.topic.id, 2)
		self.assertEqual(question.forum.name, "Outro")

	def test_add_invalid_question(self):
		result = controller.add_question(self.user, None, None, "Ad")
		self.assertEqual(result, -1)

	def test_remove_question(self):
		result = controller.remove_question(self.user, self.question.id)
		self.assertEqual(result, 0)

	def test_remove_invalid_question(self):
		result = controller.remove_question(self.user, None)
		self.assertEqual(result, -1)


class AnswersTestCase(TestCase):
	fixtures = ['forum/fixtures/forum/test_db.json']

	def setUp(self):
		self.user = User.objects.get(username="drmargarido")
		self.sol = User.objects.get(username="Solange")
		self.question = Question.objects.get(id=1)

	def test_add_answer(self):
		result = controller.add_answer(self.user, self.question.id, "It was because of the error 20323!")
		self.assertTrue(result >= 0)

	def test_invalid_add_answer(self):
		result = controller.add_answer(self.user, None, "It was because of the error 20323!")
		self.assertEquals(result, -1)

	def test_edit_answer(self):
		result = controller.edit_answer(self.user, 1, "New Description achieved")
		self.assertEquals(result, 0)
		self.assertEquals(Answer.objects.get(id=1).description, "New Description achieved")

	def test_invalid_edit_answer(self):
		result = controller.edit_answer(self.user, 1, "")
		self.assertEquals(result, -1)
		self.assertNotEquals(Answer.objects.get(id=1).description, "New Description achieved")

	def test_remove_answer(self):
		result = controller.remove_answer(self.user, 1)
		self.assertEquals(result, 0)

	def test_remove_answer_without_permission(self):
		result = controller.remove_answer(self.sol, 1)
		self.assertEquals(result, -3)