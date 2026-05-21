from django.contrib import admin

# Register your models here.
from .models import Course,user_in_course

admin.site.register(Course)
admin.site.register(user_in_course)
