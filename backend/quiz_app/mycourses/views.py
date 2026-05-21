from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from quiz_app.email_settings import *
from django.db.models import Q 
import random
import string
import hashlib


from .models import Course,user_in_course
from .serializers import CourseSerializer
from myusers.utils import getUser,getUserData,hashSHA256
from myusers.models import MyUser

@api_view(["POST"])
def create_group(request):
	user = getUser(request)
	if user is not None:
		if user.verified == True:
			group_data ={}
			group_data["course_code"] = request.data.get("course_code", "").rstrip()
			group_data["course_name"] = request.data.get("course_name", "").rstrip()
			group_data["offered_year"] = request.data.get("offered_year", "").rstrip()
			# rstrip() to removes whitespaces at the ed of the string
			serializer = CourseSerializer(data=group_data)
			if serializer.is_valid():
				courses =  Course.objects.filter(Q(course_code= group_data["course_code"]) 
												& Q(offered_year= group_data["offered_year"])).distinct()
				
				if len(courses) ==0:
					course = serializer.save()
					relation = user_in_course(user=user ,course =course, role="P",request_accepted=True)
					relation.save()
					return Response("ok" ,status= status.HTTP_200_OK)
				return Response("Group with such details exists" , status=status.HTTP_400_BAD_REQUEST)
			return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
		return Response("First Activate your account", status=status.HTTP_400_BAD_REQUEST)
	return Response("No user is logged in ", status=status.HTTP_401_UNAUTHORIZED)

def roll_full_form(current_role):
	if current_role=="S":
		return "student"
	return "professor"

@api_view(["POST"])
def send_request(request):
	user = getUser(request)
	if user is not None:
		if user.verified == True:
			course_pk = request.data.get("course_pk", "")
			course = Course.objects.filter(Q(pk= course_pk))
			if len(course) ==1:
				course = course[0]
				relation = user_in_course.objects.filter(Q(user=user) & Q(course=course))
				if len(relation)==1 :
					relation = relation[0]
					if relation.role=='P' :
						send_to_user = request.data.get("send_to_user","")
						my_user = getUserData(send_to_user)
						if my_user is not None:
							relation = user_in_course.objects.filter(Q(user=my_user) & Q(course=course)).distinct()
							if len(relation) ==0:
								if request.data.get("join_as_role","")=="S" or request.data.get("join_as_role","")=="P":
									while True:
										code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 20)) 
										temp_codes = user_in_course.objects.filter(Q(verification_code=hashlib.sha256(code.encode()).hexdigest()))
										if len(temp_codes) == 0:
											break
									# print(code,hashlib.sha256(code.encode()).hexdigest())
									newuser_in_course = user_in_course(user=my_user,course=course,role=request.data.get("join_as_role",""),\
																			verification_code=hashlib.sha256(code.encode()).hexdigest())
									newuser_in_course.save()
									content = EMAIL_CONTENT["COURSE_JOIN_REQUEST"].format(name1=my_user.username,\
													name2=user.username,course_name=course.course_name,role=roll_full_form(request.data.get("join_as_role",""))) \
													+EMAIL_BASE_LINK_COURSE_JOINING +"code=" + code +"/" 
									send_mail(EMAIL_TITLE["COURSE_JOIN_REQUEST"].format(course_code=course.course_code) , content , DEFAULT_FROM_EMAIL , [my_user.email])
									return Response({ "message": "User has been invited to the course"},status=status.HTTP_200_OK)
								return Response({ "message": "Invalid role.Not allowed"},status= status.HTTP_400_BAD_REQUEST)
							return Response({ "message": "Already sent the join request to the user" },status= status.HTTP_400_BAD_REQUEST)	
						return Response({ "message": "No such user exists to send the request to" },status= status.HTTP_400_BAD_REQUEST)
					return Response({ "message": "User is not Professor , does not have join request sending access"} , status=status.HTTP_401_UNAUTHORIZED)
				return Response({ "message": "User is not in the group , does not have join request sending access" }, status=status.HTTP_401_UNAUTHORIZED)
			return Response({ "message": "No such course exists" },status= status.HTTP_400_BAD_REQUEST)
		return Response({ "message": "First Activate your account"},status=status.HTTP_400_BAD_REQUEST)
	return Response({ "message": "No user is logged in "}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def accept_course_join(request , code):
	temp_courses = user_in_course.objects.filter(Q(verification_code=hashlib.sha256(code.encode()).hexdigest())).distinct()
	# print(hashlib.sha256(code.encode()).hexdigest())
	if len(temp_courses) == 1:
		temp_course = temp_courses[0]
		temp_course.request_accepted= True
		temp_course.verification_code = ''
		temp_course.save()		
		return HttpResponse("Successfully Added in the course")	
	return HttpResponse("Invalid request")
	

@api_view(["GET"])
def view_my_courses(request):
	user = getUser(request)
	if user is not None:
		if user.verified == True:
			courses = user_in_course.objects.filter(Q(user=user) & Q(request_accepted=True)).values()
			for i in range(len(courses)):
				my_course = courses[i]
				my_course["course"] = (Course.objects.filter(pk=courses[i]["course_id"]).values())[0]
				del my_course["course_id"]
			print(courses)
			return Response(courses,status=status.HTTP_200_OK)
		return Response("First Activate your account", status=status.HTTP_400_BAD_REQUEST)
	return Response("No user is logged in ", status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def view_course_list(request,course_pk):
	user = getUser(request)
	if user is not None:
		course = Course.objects.filter(Q(pk=course_pk)).values()
		if len(course)==1:
			current_user_in_course = user_in_course.objects.filter(Q(course=course_pk) & Q(user=user)).values()
			if len(current_user_in_course)==1:
				users_in_course = user_in_course.objects.filter(Q(course=course_pk) & Q(request_accepted=True)).distinct()
				_data_to_send = []
				for i in users_in_course:
					print(i)
					_data_to_send.append({
							"user_id":i.user.id,
							"role":i.role,
							"request_accepted":i.request_accepted,
							"username":i.user.username,
							"name":i.user.name,
							
						})
				return Response(_data_to_send,status=status.HTTP_200_OK)
			return Response("User not in course", status=status.HTTP_401_UNAUTHORIZED)
		return Response("No such course exists" ,status= status.HTTP_400_BAD_REQUEST)
	return Response("No user is logged in ", status=status.HTTP_401_UNAUTHORIZED)

# @api_view(["DELETE"])
# def delete_course(request):
# 	user = getUser(request)
# 	if user is not None:
# 		if user.verified == True:
# 			course_pk = request.data.get("course_pk", "")
# 			course = Course.objects.filter(Q(pk= course_pk))
# 			if len(course) ==1:
# 				course = course[0]
# 				relation = user_in_course.objects.filter(Q(user=user) & Q(course=course))
# 				if len(relation)==1 :
# 					relation = relation[0]
# 					if relation.role=='P' :
						
# 					return Response({ "message": "User is not Professor , does not have join request sending access"} , status=status.HTTP_401_UNAUTHORIZED)
# 				return Response({ "message": "User is not in the group , does not have join request sending access" }, status=status.HTTP_401_UNAUTHORIZED)
# 			return Response({ "message": "No such course exists" },status= status.HTTP_400_BAD_REQUEST)
# 		return Response({ "message": "First Activate your account"},status=status.HTTP_400_BAD_REQUEST)
# 	return Response({ "message": "No user is logged in "}, status=status.HTTP_401_UNAUTHORIZED)
# 	