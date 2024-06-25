from rest_framework import serializers

import json
from .models import Course,Coupon,Student,Person,Profile,User,Follow,Product

class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		model = Course
		fields = '__all__'
		
class CourseGetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields ='__all__'

class CouponSerializer(serializers.ModelSerializer):

	class Meta:
		model = Coupon
		fields = '__all__'
	
class CouponGetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupon
		fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Student
		fields ='__all__'
		depth = 1
class PersonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Person
		fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'
		depth=1

class FollowGetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Follow
		fields = '__all__'
		depth = 1

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'
		