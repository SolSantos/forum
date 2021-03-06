from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . import controller

@login_required
def get_courses(request):
	return JsonResponse({"courses": controller.get_courses()})


@login_required
def get_regular_forums(request):
	return JsonResponse({"forums": controller.get_forums_by_type("S")})


@login_required
def get_other_forums(request):
	return JsonResponse({"forums": controller.get_forums_by_type("O")})


@login_required
def get_forum(request, forum_id=""):
	if forum_id == "":
		return JsonResponse({"status": 400, "description": "Missing mandatory data"})

	return JsonResponse({"forums": controller.get_forum(forum_id)})


@login_required
def get_question(request, question_id=""):
	if question_id == "":
		return JsonResponse({"status": 400, "description": "Missing mandatory data"})

	return JsonResponse({"forums": controller.get_question(question_id)})


@login_required
def add_question(request):
	if not request.POST:
		return JsonResponse({"status": 404, "description": "Verb not supported"})

	topic_id = request.POST.get("topic_id", None)
	forum_id = request.POST.get("forum_id", None)
	description = request.POST.get("description", "")

	result = controller.add_question(request.user, topic_id, forum_id, description)
	
	if result == -1:
		return JsonResponse({"status": 400, "description": "Missing mandatory fields"})
	elif result == -2:
		return JsonResponse({"status": 404, "description": "Unknown Error"})

	return JsonResponse({"status": 200})


@login_required
def remove_question(request):
	if not request.POST:
		return JsonResponse({"status": 404, "description": "Verb not supported"})

	question_id = request.POST.get("question_id", None)

	result = controller.remove_question(request.user, question_id)
	
	if result == -1:
		return JsonResponse({"status": 400, "description": "Missing mandatory fields"})
	elif result == -2:
		return JsonResponse({"status": 400, "description": "Received Question is invalid"})
	elif result == -3:
		return JsonResponse({"status": 400, "description": "You are not the owner of the question to manage it"})

	return JsonResponse({"status": 200})


@login_required
def add_answer(request):
	if not request.POST:
		return JsonResponse({"status": 404, "description": "Verb not supported"})
	
	question_id = request.POST.get("question_id", None)
	description = request.POST.get("description", "")

	result = controller.add_answer(request.user, question_id, description)
	
	if result == -1:
		return JsonResponse({"status": 400, "description": "Missing mandatory fields"})
	elif result == -2:
		return JsonResponse({"status": 404, "description": "Received Question is invalid"})

	return JsonResponse({"status": 200})



@login_required
def edit_answer(request):
	if not request.POST:
		return JsonResponse({"status": 404, "description": "Verb not supported"})
	
	answer_id = request.POST.get("answer_id", None)
	description = request.POST.get("description", "")

	result = controller.add_answer(request.user, answer_id, description)
	
	if result == -1:
		return JsonResponse({"status": 400, "description": "Missing mandatory fields"})
	elif result == -2:
		return JsonResponse({"status": 404, "description": "Received Answer is invalid"})
	elif result == -3:
		return JsonResponse({"status": 400, "description": "You are not the owner of the answer to manage it"})

	return JsonResponse({"status": 200})


@login_required
def remove_answer(request):
	if not request.POST:
		return JsonResponse({"status": 404, "description": "Verb not supported"})

	answer_id = request.POST.get("answer_id", None)

	result = controller.remove_question(request.user, answer_id)
	
	if result == -1:
		return JsonResponse({"status": 400, "description": "Missing mandatory fields"})
	elif result == -2:
		return JsonResponse({"status": 400, "description": "Received Answer is invalid"})
	elif result == -3:
		return JsonResponse({"status": 400, "description": "You are not the owner of the answer to manage it"})

	return JsonResponse({"status": 200})