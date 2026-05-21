import string 
import random 
import hashlib

from .models import MyUser,Token

def hashSHA256(value):
	return hashlib.sha256(value.encode()).hexdigest()

def getUser(request):
    print("HEADERS == \n ",request.headers)
    if "Authorization" in request.headers:
    	token = request.headers["Authorization"]
    	if len(token)==20:
    		token = hashSHA256(token)
    		token = Token.objects.filter(token = token)
    		if len(token) ==1:
    			return token[0].user
    print(request.headers)
    return None

def getUserData(username):
    users = MyUser.objects.filter(username=username)
    if len(users)==1:
        return users[0]
    return None

def getUserByPk(pk):
    users = MyUser.objects.filter(pk=pk)
    if len(users)==1:
        return users[0]
    return None