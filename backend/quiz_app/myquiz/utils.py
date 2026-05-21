import pytz 
import tzlocal



from rest_framework import status
from django.db.models import Q 

from mycourses.models import Course,user_in_course
from .models import *

def user_in_course_details(user,course_pk):
	user_course_util_data = {}
	course = "Not Valid"
	if user is not None:
		if user.verified == True:
			if course_pk!="":
				courses = Course.objects.filter(Q(pk=course_pk))
				if len(courses)==1:
					course = courses[0]
					relation = user_in_course.objects.filter(Q(user = user.pk) & Q(course=course_pk)).distinct()
					# print(relation,len(relation))
					if len(relation)==1:
					    user_course_util_data["allowed"] =True
					    user_course_util_data["relation"] = relation[0].role 
					else:
						user_course_util_data["allowed"] = False
						user_course_util_data["error_message"] = "User is not the part of the course" 
						user_course_util_data["status"] = status.HTTP_401_UNAUTHORIZED 
				else:
					user_course_util_data["allowed"] = False
					user_course_util_data["error_message"] = "No such course is found"
					user_course_util_data["status"] = status.HTTP_400_BAD_REQUEST 
			else:
				user_course_util_data["allowed"] = False
				user_course_util_data["error_message"] = "course_pk should not be empty"
				user_course_util_data["status"] = status.HTTP_400_BAD_REQUEST 
		else:
			user_course_util_data["allowed"] = False
			user_course_util_data["error_message"] = "First Activate your account"
			user_course_util_data["status"] = status.HTTP_400_BAD_REQUEST 
	else:
		user_course_util_data["allowed"] = False
		user_course_util_data["error_message"] = "No user is logged in"
		user_course_util_data["status"] = status.HTTP_401_UNAUTHORIZED 
	return user_course_util_data,course

def marks_for_a_question(question_type,question_answer,student_answer,positive_marks,negtive_marks,partial_allowed,option_count):
	if question_type!="M" or partial_allowed==False:
		if 	question_answer==student_answer:
			return positive_marks
		return -1*negtive_marks
	student_options = student_answer.split(';')
	correct_options = question_answer.split(';')
	for i in student_options:
		if i not in correct_options:
			return -1*negtive_marks
	if len(student_options)==len(correct_options):
		return positive_marks
	return (len(student_options)/option_count)*positive_marks

def delete_every_information_for_a_quiz(quiz_pk):
	question_in_current_quiz = question_in_quiz.objects.filter(Q(quiz=quiz_pk))
	questions = [_q.question for _q in question_in_current_quiz]
	question_pks = [_q.question.pk for _q in question_in_current_quiz]
	option_in_quiz = []
	for _q_pk in question_pks:
		current_options = Option_in_question.objects.filter(Q(question=_q_pk))
		for _o in current_options:
			option_in_quiz.append(_o.option)
	print(questions)
	print(option_in_quiz)
	quiz_attempt_response = quiz_quizattempt.objects.filter(Q(quiz=quiz_pk))
	# print(quiz_attempt_response)
	current_quiz_attempts = [_qa.quiz_attempt for _qa in quiz_attempt_response]
	print(current_quiz_attempts)	
	for q in questions:
		q.delete()
	for o in option_in_quiz:
		o.delete()
	for qa in current_quiz_attempts:
		qa.delete()
	current_quiz = Quiz.objects.filter(Q(pk=quiz_pk))
	current_quiz.delete()

def find_quiz_attempt_with_user_and_quiz(user,quiz):
	attempts = quiz_quizattempt.objects.filter(Q(quiz=quiz))
	for qa in attempts:
		final_attempts = user_quizattempt.objects.filter(Q(user=user) & Q(quiz_attempt=qa.quiz_attempt))
		if len(final_attempts)>0:
			return qa.quiz_attempt
	return None

def time_formating(_time):
	ltz = tzlocal.get_localzone()
	localtz = _time.replace(tzinfo=pytz.utc).astimezone(ltz)
	return localtz.strftime('%H:%M %d %b,%Y')