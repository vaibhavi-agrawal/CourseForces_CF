from django.db import models
from myusers.models import MyUser

# Create your models here.

role_options = [
	("P","Professor"),
	("S","Student")
]

class Course(models.Model):
	course_code = models.CharField(max_length=10)
	course_name = models.CharField(max_length=50)
	offered_year = models.CharField(max_length=40 )

class user_in_course(models.Model):
	user = models.ForeignKey(MyUser , on_delete = models.CASCADE)
	course = models.ForeignKey(Course , on_delete=models.CASCADE)
	role = models.CharField(max_length=1, choices = role_options) 
	request_accepted = models.BooleanField(default = False)
	verification_code = models.CharField(max_length = 66,null=True ,blank=True)
