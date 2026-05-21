# from rest_framework import serializers
# from .models import MyUser,Token
# from django.core.mail import send_mail
# from django.conf import settings

# class RegisterSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = MyUser
# 		fields = "__all__"

# 	# def create(self, validated_data):
# 	# 	return MyUser.objects.create(**validated_data)
# 	def create(self, validated_data):
#     user = MyUser.objects.create(**validated_data)
# 	send_mail(
#             'Activate your account',
#             'Your account has been created successfully.',
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False
#         )

#         return user

# 	def update(self , instance, validated_data):
# 		for key,value in validated_data.items():
# 			setattr(instance, key ,value)
# 		instance.save()
# 		return instance 

# class TokenSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Token
# 		fields = "__all__"

# 	def create(self, validated_data):
# 		return Token.objects.create(**validated_data)

# 	def update(self , instance, validated_data):
# 		for key,value in validated_data.items():
# 			setattr(instance, key ,value)
# 		instance.save()
# 		return instance 

from rest_framework import serializers
from .models import MyUser, Token
from django.core.mail import send_mail
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = "__all__"

    def create(self, validated_data):

        user = MyUser.objects.create(**validated_data)

        send_mail(
            'Activate your account',
            'Your account has been created successfully.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = "__all__"

    def create(self, validated_data):
        return Token.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance