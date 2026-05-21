import random
import string
import hashlib
import bcrypt

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from quiz_app.email_settings import *
from django.core.mail import send_mail
from django.db.models import Q 

from .utils import getUser,hashSHA256

from .serializers import (
	RegisterSerializer,TokenSerializer
)

from .models import (
    MyUser,Token
)

def HashPass(password):
    password=password.encode()
    return bcrypt.hashpw(password,bcrypt.gensalt())

def pass_checker(old,password):
    return bcrypt.checkpw(old.encode(),password)

@api_view(["POST"])
def user_register(request):
	print(request.data)
	register_data ={}
	register_data["name"] = request.data.get("name","")
	register_data["username"] = request.data.get("username","")
	register_data["department"] = request.data.get("department","")
	register_data["email"] = request.data.get("email","")
	if '@' in register_data["username"]:
		return Response("username cannot contain '@' symbol", status=status.HTTP_400_BAD_REQUEST)

	other_user = MyUser.objects.filter(email=register_data["email"]).first()
	if other_user:
		if other_user.verified:
			return Response("User with that emailID is registered", status=status.HTTP_401_UNAUTHORIZED)
		other_user.delete()

	other_username = MyUser.objects.filter(username=register_data["username"]).first()
	if other_username:
		if other_username.verified:
			return Response("Username is already taken", status=status.HTTP_400_BAD_REQUEST)
		other_username.delete()

	password1 = request.data.get("password","")
	password2 = request.data.get("confirm_password","")
	if password2 == password1:
		if len(password2)>=4:
			code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 20)) 
			register_data["verification_code"] = hashlib.sha256(code.encode()).hexdigest()
			register_data["password"]=HashPass(password1).decode()
			serializer = RegisterSerializer(data = register_data)
			if serializer.is_valid():
				serializer.save()
				activation_link = EMAIL_BASE_LINK + "activate/" + register_data["username"] + "/code=" + code + "/"
				content = EMAIL_CONTENT["ACTIVATION"].format(name=register_data["username"]) + activation_link
				try:
					send_mail(EMAIL_TITLE["ACTIVATION"], content, DEFAULT_FROM_EMAIL, [register_data["email"]])
				except Exception as e:
					print("Activation email failed:", e)
					print("Activation link:", activation_link)
				return Response({
					"message": "Registered successfully. Check your email to activate your account before signing in.",
					"activation_link": activation_link,
				}, status=status.HTTP_200_OK)
			return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
		return Response("Password must be atleast 4 characters",status=status.HTTP_400_BAD_REQUEST)
	return Response("Password must be same", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def activate(request , username, code):
	user= get_object_or_404(MyUser, username=username)
	hashed_code = hashlib.sha256(code.encode()).hexdigest()
	if user.verified == True:
		return HttpResponse("Invalid Request") 
		# Response("Invalid Request",status = status.HTTP_401_UNAUTHORIZED) 
	else: #if user.verified == False
		if user.verification_code==hashed_code:
			user.verified= True
			user.verification_code = ''
			user.save()
			return HttpResponse("Successfully activated Your Account")
		return HttpResponse("Invalid Request") 


@api_view(["POST"])
def user_login(request):
	print("yoyo")
	user = getUser(request)
	if user is None:
		print(request.data)
		value = request.data.get("value" ,"")
		if len(value)>0:
			users = MyUser.objects.filter(Q(username=value) | Q(email=value)).distinct()
			if len(users) ==1:
				if users[0].verified == True:
					password = request.data.get("password","")
					if pass_checker(password,users[0].password.encode()):
						while True:
							code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 20)) 
							token = hashSHA256(code)
							serializer = TokenSerializer(data={"token":token , "user":users[0].pk})
							if serializer.is_valid():
								serializer.save()
								break
							print(serializer.errors)
						x = {
							"message":"Successfully logged in",
							"token":code,
							"name":users[0].name,
							"username":users[0].username,
							"department":users[0].department,
							"email":users[0].email
						}
						print(x)
						return Response(
							{
								"message":"Successfully logged in",
								"token":code,
								"name":users[0].name,
								"username":users[0].username,
								"department":users[0].department,
								"email":users[0].email
							}, status=status.HTTP_200_OK)
					return Response({"message" : "Wrong Password"} ,status=status.HTTP_401_UNAUTHORIZED)
				return Response({"message":"First activate the user."} ,status=status.HTTP_400_BAD_REQUEST) 
			return Response({"message":"There is no user registered with "+ value + " username/email" }, status=status.HTTP_400_BAD_REQUEST)
		return Response({"message":"Email/username field should be non empty"}, status=status.HTTP_400_BAD_REQUEST)
	return Response({"message":"User is already logged in"} , status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def user_logout(request):
	print("Heheheh")
	user = getUser(request)
	if user is not None:
		token = hashSHA256(request.headers["Authorization"])
		my_token = get_object_or_404(Token, token=token)
		my_token.delete()
		return Response("Succesfully logged out" , status=status.HTTP_200_OK)
	return Response("No user logged in", status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def forgot_password1(request):
	user = getUser(request)
	if user is None:
		value = request.data.get("value" ,"")
		if len(value)>0:
			users = MyUser.objects.filter(Q(username=value) | Q(email=value)).distinct()
			if len(users) ==1:
				user = users[0]
				if user.verified == True:
					code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 20)) 
					user.verification_code = hashSHA256(code)
					user.save()
					content = EMAIL_CONTENT["FORGOT_PASSWORD"].format(name=user.username) +EMAIL_BASE_LINK +'password/forgot/2/' + user.username +"/code=" + code +"/" 
					send_mail(EMAIL_TITLE["FORGOT_PASSWORD"] , content , DEFAULT_FROM_EMAIL , [user.email])
					return Response("verification code sent", status=status.HTTP_200_OK)
				return Response("Please first activate your account by clicking on the activation link sent to your email" ,status=status.HTTP_400_BAD_REQUEST)
			return Response("User is not registered with us" , status=status.HTTP_400_BAD_REQUEST)
		return Response("email/username cannot be empty" ,status=status.HTTP_400_BAD_REQUEST)
	return Response("The user is logged in .Try after logging out", status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def forgot_password2(request,username,code):
	user = getUser(request)
	if user is None:
		users = MyUser.objects.filter(Q(username=username)).distinct()
		if len(users) ==1:
			user = users[0]
			if user.verified == True:
				code= hashSHA256(code)
				if code == user.verification_code:
					new1 = request.data.get("new_password1","")
					new2 = request.data.get("new_password2","")
					if new1 == new2:
						if len(new1)>=4:
							new = HashPass(new1).decode()
							user.password = new
							user.verification_code=""
							user.save()
							return Response("Password changed Successfully" ,status=status.HTTP_200_OK)		
						return Response("Password must contain 4 characters", status=status.HTTP_400_BAD_REQUEST)
					return Response("Password must be same", status=status.HTTP_400_BAD_REQUEST)
				return Response("Invalid verification code", status=status.HTTP_401_UNAUTHORIZED)
			return Response("Please first activate your account by clickink on the activation link sent to the emailid" ,status=status.HTTP_400_BAD_REQUEST)
		return Response("User is not registered with us" , status=status.HTTP_400_BAD_REQUEST)
	return Response("The user is logged in .Try after logging out", status=status.HTTP_400_BAD_REQUEST)
