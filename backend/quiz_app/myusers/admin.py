from django.contrib import admin

# Register your models here.
from .models import MyUser,Token

admin.site.register(MyUser)
admin.site.register(Token)
