from django.urls import path,include

from .views import (
    user_register,activate,user_login,user_logout,forgot_password1,forgot_password2
)

urlpatterns = [
	path('register/',user_register, name="user_register"),
	path('activate/<str:username>/code=<str:code>/' ,activate, name="activate"),
	path('auth/login/',user_login, name="user_login"),
	path('auth/logout/',user_logout, name="user_logout"),
	path('password/forgot/1/',forgot_password1, name="forgot_password1"),
	path('password/forgot/2/<str:username>/code=<str:code>/',forgot_password2, name="forgot_password2"),
]