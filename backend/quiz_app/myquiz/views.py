import json
from django.utils import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from .models import *
from .utils import user_in_course_details,marks_for_a_question,delete_every_information_for_a_quiz,find_quiz_attempt_with_user_and_quiz,time_formating
from .serializers import QuizSerializer,QuestionSerializer,OptionSerializer,QuizAttemptSerializer
from myusers.utils import getUser
from django.db.models import Q 
from quiz_app.email_settings import *
from django.core.mail import send_mail


@api_view(["POST"])
def add_quiz(request):
	user = getUser(request)
	# print(user)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			# if request.method == "POST":
			quiz_data = {}
			quiz_data["title"] = request.data.get("title" ,"")
			quiz_data["content"] = request.data.get("content", "")
			quiz_data["deadline"] = request.data.get("deadline","")
			quiz_data["start_at"] = request.data.get("start_at","")
			serializer = QuizSerializer(data = quiz_data)
			if serializer.is_valid():				
				quizes = Quiz.objects.filter(Q(title=quiz_data["title"]))
				for temp_quiz in quizes:
					quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course.id) & Q(quiz=temp_quiz)).distinct()
					# print("YOYO ",quiz_in_course_relations,len(quiz_in_course_relations))
					if len(quiz_in_course_relations)>0:
						return Response("Quiz with the same title exists in the course", status=status.HTTP_400_BAD_REQUEST)
				quiz_response = serializer.save()
				# print(a)
				new_quiz_in_course_relation = quiz_in_course(course=course,quiz=quiz_response)
				new_quiz_in_course_relation.save()
				return	Response({
					"quiz_pk":quiz_response.pk,
					"message":"Successfully created Quiz!"
					} ,status=status.HTTP_200_OK)
			return Response({"message":"errors",
							"error":serializer.errors }
							, status=status.HTTP_400_BAD_REQUEST) 
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])

@api_view(["GET"])
def quiz_in_a_course_list(request,course_pk):
	user = getUser(request)
	util_data,course = user_in_course_details(user,course_pk)
	if util_data["allowed"]:
		quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course_pk))
		course_data = {
			"quiz_list" : []
		}
		j = 0 
		for i in quiz_in_course_relations:
			_current_quiz_questions = question_in_quiz.objects.filter(Q(quiz=i.quiz.pk))
			_current_quiz_data = {
				"pk":i.quiz.pk,
				"title":i.quiz.title,
				"content":i.quiz.content,
				"deadline":time_formating(i.quiz.deadline),
				"start_at":time_formating(i.quiz.start_at),				
				"answer_key_visible":i.quiz.answer_key_visible,	
				"num":len(_current_quiz_questions),
				"show_submit_button":True,
				"show_total_score":False,
				"show_take_quiz":False
			}
			current_user_quiz_attempt = find_quiz_attempt_with_user_and_quiz(user,i.quiz)
			if util_data["relation"] == 'P' or current_user_quiz_attempt is not None:
				_current_quiz_data["show_submit_button"] = False
			if current_user_quiz_attempt is not None and i.quiz.checked:
				current_user_marks_details = json.loads(current_user_quiz_attempt.total_marks)
				_current_quiz_data["show_total_score"] = True 
				_current_quiz_data["total_score"] =  current_user_marks_details["total"]
			if util_data["relation"] == 'P' or (util_data["relation"] == 'S' and timezone.now()>=i.quiz.start_at):
				_current_quiz_data["show_take_quiz"] = True
			course_data["quiz_list"].append(_current_quiz_data)
		course_data["message"]="ok"
		print(course_data)
		return Response(course_data,status=status.HTTP_200_OK)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])


@api_view(["POST"])
def add_question(request):
	user = getUser(request)
	# print(user)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			quiz_pk = request.data.get("quiz_pk", "")
			if quiz_pk!="":
				quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk)).distinct()
				if len(quiz_in_course_relations)==1:
					question_data = {}
					question_data["content"] = request.data.get("content" ,"")
					question_data["answer"] = request.data.get("answer","")
					question_data["positive_marks"] = request.data.get("positive_marks","")
					question_data["negative_marks"] = request.data.get("negative_marks","")
					question_data["question_type"] = request.data.get("question_type","")
					question_data["partial_allowed"] = request.data.get("partial_allowed","")
					question_serializer = QuestionSerializer(data = question_data)
					option_serialisers_results = []
					if question_serializer.is_valid():				
						option_serialisers = []
						correct_answers_index = []
						if question_data["question_type"] == "S" or question_data["question_type"] == "M": 
							question_data["options"] = request.data.get("options",[])
							index = 0
							for _temp_option_data in question_data["options"]:
								print(_temp_option_data)
								if "option_value" not in _temp_option_data.keys() or "is_correct" not in _temp_option_data.keys():
									return Response({"message":"Option at index "+str(index)+" has wrong format"},status=status.HTTP_400_BAD_REQUEST)
								_current_option_serialiser = OptionSerializer(data={"option_value":_temp_option_data["option_value"]})
								if _current_option_serialiser.is_valid():
									option_serialisers.append(_current_option_serialiser)
								else:
									return Response({
											"message":"error",
											"errors":_current_option_serialiser.errors
										} , status=status.HTTP_400_BAD_REQUEST)
								if _temp_option_data["is_correct"]==True:
									correct_answers_index.append(index)
								index+=1
							if len(option_serialisers)<1 or len(option_serialisers)>5 or len(correct_answers_index)==0:
								return Response({"message":"A question must have total number of options in range 1 to 5 and have atleast one answer correct"}, status=status.HTTP_400_BAD_REQUEST)
							if 	question_data["question_type"] == "S" and len(correct_answers_index)>1:
								return Response({"message":"A single correct type can have exactly one correct answer"},status=status.HTTP_400_BAD_REQUEST)
							index = 0
							_answer_pks= []
							for _temp_serializer in option_serialisers:
								_current_option_results = _temp_serializer.save()
								option_serialisers_results.append(_current_option_results)
								# print(index,correct_answers_index,index in correct_answers_index)
								if index in correct_answers_index:
									_answer_pks.append(str(_current_option_results.pk))
								index+=1
							# print(_answer_pks)
							question_data["answer"] = ";".join(_answer_pks)
							question_serializer = QuestionSerializer(data = question_data)
							if question_serializer.is_valid():
								pass
							else:
								return Response(question_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
						question_response = question_serializer.save()
						for _temp_option in option_serialisers_results:
							option_in_question_relation = Option_in_question(question=question_response,option=_temp_option)
							option_in_question_relation.save()
						new_question_in_quiz_relation = question_in_quiz(question=question_response,quiz=quiz_in_course_relations[0].quiz)
						new_question_in_quiz_relation.save()
						return Response({
							"question_pk":question_response.pk,
							"message":"Succesully created Question"
							},status=status.HTTP_200_OK)
					return Response({
							"message":"error",
							"errors":question_serializer.errors
						} , status=status.HTTP_400_BAD_REQUEST)
				return Response({"message":"No such quiz found in the course"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message":"quiz_pk should not be empty"},status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])

@api_view(["DELETE"])
def delete_question(request):
	user = getUser(request)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			quiz_pk = request.data.get("quiz_pk", "")
			if quiz_pk!="":
				quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk))
				if len(quiz_in_course_relations)==1:
					question_pk = request.data.get("question_pk", "")
					if question_pk!="":
						question_in_quiz_relations = question_in_quiz.objects.filter(Q(question=question_pk) & Q(quiz=quiz_pk))
						if len(question_in_quiz_relations)==1:
							question_relations = Question.objects.filter(Q(pk=question_pk))
							options_in_questions_relations = Option_in_question.objects.filter(Q(question=question_pk))
							for _option in options_in_questions_relations:
								option_relation = Option.objects.filter(Q(pk=_option.option.pk))
								option_relation.delete()
							question_relations.delete()
							return Response({"message":"Succesfully deleted the question"},status=status.HTTP_200_OK)
						return Response({"message":"No such question found in the quiz"}, status=status.HTTP_400_BAD_REQUEST)
					return Response({"message":"question_pk should not be empty"},status=status.HTTP_400_BAD_REQUEST)
				return Response({"message":"No such quiz found in the course"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message":"quiz_pk should not be empty"},status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])

@api_view(["GET"])
def view_quiz_questions(request,course_pk, quiz_pk):
	user = getUser(request)
	# print(user)
	util_data,course = user_in_course_details(user,course_pk)
	if util_data["allowed"]:
		quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk)).distinct()
		# print(quiz_in_course_relations)
		if len(quiz_in_course_relations)==1:
			quiz_data = {
				"title":quiz_in_course_relations[0].quiz.title,
				"content":quiz_in_course_relations[0].quiz.content,
				"start_at":time_formating(quiz_in_course_relations[0].quiz.start_at),
				"deadline":time_formating(quiz_in_course_relations[0].quiz.deadline),
				# "answer_key_visible":quiz_in_course_relations[0].quiz.answer_key_visible,
				"questions":[]
			}
			# time_formating(quiz_in_course_relations[0].quiz.start_at)
			# print("AAAAAAAAAAAAAAAAAAAA\n\n")
			question_relation = question_in_quiz.objects.filter(Q(quiz=quiz_pk))
			current_user_quiz_attempt = find_quiz_attempt_with_user_and_quiz(user,quiz_in_course_relations[0].quiz)
			current_user_marks_details = {}
			if current_user_quiz_attempt is not None and quiz_in_course_relations[0].quiz.checked==True:
				current_user_marks_details = json.loads(current_user_quiz_attempt.total_marks)

			for _ques in question_relation:
				_current_question_data = {
					"question_pk":_ques.question.pk,
					"content":_ques.question.content,
					"question_type":_ques.question.question_type, 
					"positive_marks":_ques.question.positive_marks,
					"negative_marks":_ques.question.negative_marks,
					"partial_allowed":_ques.question.partial_allowed
				}
				options_data = {}
				if _ques.question.question_type=="M" or _ques.question.question_type=="S":
					_current_question_data["options"] = []
					options_in_questions_relations = Option_in_question.objects.filter(Q(question=_ques.question.pk))
					for _option in options_in_questions_relations:
						_curent_option_data = {
							"option_value":_option.option.option_value,
							"option_pk":_option.option.pk
						}
						options_data[str(_option.option.pk)] = _option.option.option_value
						_current_question_data["options"].append(_curent_option_data)
				print(options_data)
				_current_question_data["correct_answer_visible"] = False
				if util_data["relation"]=='P' or quiz_in_course_relations[0].quiz.answer_key_visible==True:
					_current_question_data["correct_answer_visible"] = True 
					if _ques.question.question_type=="M" or _ques.question.question_type=="S":
						correct_options = _ques.question.answer.split(';')
						print(correct_options)
						print(options_data[correct_options[0]])
						correct_answers_values = [options_data[x] for x in correct_options]
						_current_question_data["correct_answer"] = ','.join(correct_answers_values)
					else:
						_current_question_data["correct_answer"] = _ques.question.answer 
				_current_question_data["user_answer_visible"] = False
				_current_question_data["your_score_visible"] = False
				if util_data["relation"]=='S':
					if current_user_quiz_attempt is not None:
						qqa = question_attempt.objects.filter(Q(question=_ques.question) & Q(quiz_attempt=current_user_quiz_attempt))
						qqa = qqa[0]
						_current_question_data["user_answer_visible"] = True 
						if _ques.question.question_type=="M" or _ques.question.question_type=="S":
							user_options = qqa.student_answer.split(';')
							user_answers_values = [options_data[x] for x in user_options]
							_current_question_data["user_answer"] = ','.join(user_answers_values)
						else:
							_current_question_data["user_answer"] = qqa.student_answer
						if quiz_in_course_relations[0].quiz.checked == True:
							_current_question_data["your_score_visible"] = True 
							_current_question_data["your_score"] = current_user_marks_details[str(_ques.question.pk)]

				quiz_data["questions"].append(_current_question_data)
				print(quiz_data)
			return Response(quiz_data,status=status.HTTP_200_OK)
		return Response("No such quiz found in the course", status=status.HTTP_400_BAD_REQUEST)
	return Response(util_data["error_message"], status=util_data["status"])

@api_view(["POST"])
def make_a_quiz_submission(request):
	print(request.data)
	print("0------")
	user = getUser(request)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'S': 
			quiz_pk = request.data.get("quiz_pk", "")
			if quiz_pk!="":
				quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk))
				if len(quiz_in_course_relations)==1:
					question_relation = question_in_quiz.objects.filter(Q(quiz=quiz_pk))
					if timezone.now()<quiz_in_course_relations[0].quiz.start_at:
						return Response({"message":"Quiz has not started, not considered a valid submission"},status=status.HTTP_400_BAD_REQUEST)
					if timezone.now()>quiz_in_course_relations[0].quiz.deadline:
						return Response({"message":"Quiz was submitted after the deadline, not considered a valid submission"},status=status.HTTP_400_BAD_REQUEST)
					question_data = {}
					for i in question_relation:
						_ques = i.question
						question_data[_ques.pk] =  {
							"question_type":_ques.question_type
						}
						if _ques.question_type=="M" or _ques.question_type=="S":
							question_data[_ques.pk]["options"] = []
							_ques_options = Option_in_question.objects.filter(Q(question=_ques))
							for _option in _ques_options:
								question_data[_ques.pk]["options"].append(_option.option.pk)

					print(question_data)
					user_question_attempts = []
					for _ques_response in request.data.get("ques_response",[]):
						if _ques_response.get("question_pk","") in question_data.keys() and "answer" in _ques_response:
							_ques_data = question_data[_ques_response.get("question_pk","")]
							print(_ques_data)
							if _ques_data["question_type"]=="M" or _ques_data["question_type"]=="S":
								if isinstance(_ques_response["answer"],list):
									for _selected_option_id in _ques_response["answer"]:
										print(_selected_option_id,_ques_data["options"])
										if _selected_option_id not in _ques_data["options"]:
											return Response("Invalid option id sent",status=status.HTTP_400_BAD_REQUEST)
									if _ques_data["question_type"]=="S" and len(_ques_response["answer"])>1:
										return Response({"message":"Only one option can be selected in Single correct question"},status=status.HTTP_400_BAD_REQUEST)
									user_question_attempts.append(
											{
												"student_answer":";".join([str(x) for x in _ques_response["answer"]]),
												"question":_ques_response.get("question_pk","")
											}) 
								else:
									return Response({"message":"Answer to a single/multi correct question should be a list of ids of options selected"}, status=status.HTTP_400_BAD_REQUEST)
							else:
								user_question_attempts.append(
									{
										"student_answer":_ques_response["answer"],
										"question":_ques_response.get("question_pk","")
									}) 
						else:
							return Response({"message":"Found a question either not having question_pk or does not belong to the course or answer not given"},status=status.HTTP_400_BAD_REQUEST)
					# quiz_attempt= QuizAttempt(submitted=request.data.get("submitted", False))
					if len(question_relation) != len(user_question_attempts):
						return Response({"message":"Number of question in quiz and the submission are different"},status=status.HTTP_400_BAD_REQUEST)
					
					attempt_serialiser = QuizAttemptSerializer(data={
							"submitted":True
						})
					if not attempt_serialiser.is_valid():
						return Response({"error":attempt_serialiser.errors()},status=status.HTTP_400_BAD_REQUEST)
					quiz_attempt_response = attempt_serialiser.save()
					print(quiz_attempt_response)
					_user_quizattempt = user_quizattempt(user=user,quiz_attempt=quiz_attempt_response)
					_user_quizattempt.save()
					_current_quiz = Quiz.objects.filter(Q(pk=quiz_pk))
					_quiz_quizattempt = quiz_quizattempt(quiz=_current_quiz[0],quiz_attempt=quiz_attempt_response)
					_quiz_quizattempt.save()
					for q in user_question_attempts:
						# print(q["question"])
						_current_question = Question.objects.filter(Q(pk=q["question"]))
						qa = question_attempt(question=_current_question[0],quiz_attempt=quiz_attempt_response,student_answer=q["student_answer"])
						qa.save()
					return Response({
							"message":"Succesully submitted the quiz response",
							"quiz_attempt_pk":quiz_attempt_response.pk
						},status=status.HTTP_200_OK)
				return Response({"message":"No such quiz found in the course"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message":"quiz_pk should not be empty"},status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"You are not Student in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])

@api_view(["GET"])
def view_quiz_marks_list(request,course_pk, quiz_pk):
	user = getUser(request)
	util_data,course = user_in_course_details(user,course_pk)
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk)).distinct()
			# print(quiz_in_course_relations)
			if len(quiz_in_course_relations)==1:
				attempts = quiz_quizattempt.objects.filter(Q(quiz=quiz_pk))
				return_data = []
				for i in attempts:
					current_user_attempt = user_quizattempt.objects.filter(Q(quiz_attempt=i.quiz_attempt))
					print(current_user_attempt)
					print(i)
					user_marks = json.loads(i.quiz_attempt.total_marks)

					return_data.append({
							"name":current_user_attempt[0].user.name,
							"username":current_user_attempt[0].user.username,
							"user_pk":current_user_attempt[0].user.pk,
							"total_marks":user_marks["total"]
						})

				return Response(return_data,status=status.HTTP_200_OK)
			return Response({"message":"No such quiz found in the course"}, status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])

@api_view(["POST"])
def calculate_all_student_marks(request):
	user = getUser(request)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			quiz_pk = request.data.get("quiz_pk", "")
			if quiz_pk!="":
				quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk))
				if len(quiz_in_course_relations)==1:
					if timezone.now()<quiz_in_course_relations[0].quiz.deadline:
						return Response({"message":"Quiz cannot be checked before the deadline, try after the deadline is over"},status=status.HTTP_400_BAD_REQUEST)
					
					attempts = quiz_quizattempt.objects.filter(Q(quiz=quiz_pk))
					for qa in attempts:
						current_user_question_attempts = question_attempt.objects.filter(Q(quiz_attempt=qa.quiz_attempt))
						current_user_marks = 0
						current_user_details = {}
						for ques in current_user_question_attempts:
							current_options = Option_in_question.objects.filter(Q(question=ques.question)).values()
							option_count = len(current_options)
							current_ques_marks = marks_for_a_question(ques.question.question_type,ques.question.answer,\
														ques.student_answer,ques.question.positive_marks,ques.question.negative_marks,ques.question.partial_allowed,option_count)
							current_user_details[str(ques.question.pk)] = current_ques_marks
							current_user_marks+=current_ques_marks
						current_user_details["total"] = current_user_marks
						print(current_user_details)
						current_user_email_title = EMAIL_TITLE["COURSE_QUIZ_CHECK"].format(quiz_title=quiz_in_course_relations[0].quiz.title,course_code=course.course_code)
						user_quizattempt_response = user_quizattempt.objects.filter(Q(quiz_attempt=qa.quiz_attempt))
						current_user_email_content = EMAIL_CONTENT["COURSE_QUIZ_CHECK"].format(name1=user_quizattempt_response[0].user.username,quiz_title=quiz_in_course_relations[0].quiz.title,course_code=course.course_code,score=str(current_user_marks))
						print("SENDING MAIL TO ",user_quizattempt_response[0].user.email)
						send_mail(current_user_email_title , current_user_email_content , DEFAULT_FROM_EMAIL , [user_quizattempt_response[0].user.email])
						qa.quiz_attempt.total_marks=json.dumps(current_user_details)
						qa.quiz_attempt.save()			
					current_quiz = Quiz.objects.filter(Q(pk=quiz_pk))
					current_quiz = current_quiz[0]
					current_quiz.checked = True 
					current_quiz.answer_key_visible = True
					current_quiz.save()
					return Response({"message":"calculated all student marks"},status=status.HTTP_200_OK)
				return Response({"message":"No such quiz found in the course"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message":"quiz_pk should not be empty"},status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])

@api_view(["DELETE"])
def delete_a_quiz(request):
	user = getUser(request)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			quiz_pk = request.data.get("quiz_pk", "")
			if quiz_pk!="":
				quiz_in_course_relations = quiz_in_course.objects.filter(Q(course=course) & Q(quiz=quiz_pk))
				if len(quiz_in_course_relations)==1:
					delete_every_information_for_a_quiz(quiz_pk)
					return Response({"message":"Succesfully deleted the quiz"},status=status.HTTP_200_OK)
				return Response({"message":"No such quiz found in the course"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message":"quiz_pk should not be empty"},status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])
	
@api_view(["DELETE"])
def delete_a_course(request):
	user = getUser(request)
	util_data,course = user_in_course_details(user,request.data.get("course_pk",""))
	if util_data["allowed"]:
		if util_data["relation"] == 'P': 
			quiz_in_course_response = quiz_in_course.objects.filter(Q(course=course))
			print(quiz_in_course_response)
			for _quiz in quiz_in_course_response:
				delete_every_information_for_a_quiz(_quiz.quiz.pk)
			course.delete()
			return Response({"message":"Succesfully deleted the course"},status=status.HTTP_200_OK)
		return Response({"message":"You are not Professor in the course"},status=status.HTTP_401_UNAUTHORIZED)
	return Response({"message":util_data["error_message"]}, status=util_data["status"])
