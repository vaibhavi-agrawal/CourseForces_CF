from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = "__all__"

	def create(self, validated_data):
		return Course.objects.create(**validated_data)

	def update(self , instance, validated_data):
		for key,value in validated_data.items():
			setattr(instance, key ,value)
		instance.save()
		return instance 

