from rest_framework import serializers
from .models import Quiz,Question,Option,QuizAttempt

class QuizSerializer(serializers.ModelSerializer):
	class Meta:
		model = Quiz
		fields = "__all__"

	def create(self, validated_data):
		return Quiz.objects.create(**validated_data)

	def update(self , instance, validated_data):
		for key,value in validated_data.items():
			setattr(instance, key ,value)
		instance.save()
		return instance 

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = "__all__"

	def create(self, validated_data):
		return Question.objects.create(**validated_data)

	def update(self , instance, validated_data):
		for key,value in validated_data.items():
			setattr(instance, key ,value)
		instance.save()
		return instance 

class OptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = "__all__"

	def create(self, validated_data):
		return Option.objects.create(**validated_data)

	def update(self , instance, validated_data):
		for key,value in validated_data.items():
			setattr(instance, key ,value)
		instance.save()
		return instance 

class QuizAttemptSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuizAttempt
		fields = "__all__"

	def create(self, validated_data):
		return QuizAttempt.objects.create(**validated_data)

	def update(self , instance, validated_data):
		for key,value in validated_data.items():
			setattr(instance, key ,value)
		instance.save()
		return instance 

