from django.shortcuts import render
import random
import string
import ast
import pdfkit
import tempfile
import os
from django.core.mail import EmailMultiAlternatives
from myapp.models import User,UserOtp,BlogPost,Likes,Course,Coupon,Student,Person,Profile,Follow,Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from random import randint
from django.db.models import Count
from . permissions import IsAllowedToWrite
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (CourseSerializer,CouponSerializer,CourseGetSerializer,
							CouponGetSerializer,StudentSerializer,PersonSerializer,ProfileSerializer,
							FollowGetSerializer,ProductSerializer)
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
from django.template.loader import get_template
from rest_framework import status
import base64


from django.http import HttpResponse


@api_view(['POST'])
@csrf_exempt
def signup(request):
	if request.method == 'POST':
		first_name = request.data.get('first_name')
		last_name = request.data.get('last_name')
		email = request.data.get('email')
		phonenumber = request.data.get('phonenumber')
		password = request.data.get('password')
		confirm_password = request.data.get('confirm_password')
		if not email or not password or not first_name or not last_name:
			return JsonResponse({'success':False,'message':'please provide required fields'})
		if not first_name.isalpha():
			return JsonResponse({'success':False,'message':'first_name cotains only alphabits'})
		if not last_name.isalpha():
			return JsonResponse({'success':False,'message':'last_name cotains only alphabits'})
		email= email.lower()
		
		if User.objects.filter(email__iexact=email).exists():
			return JsonResponse({'success':False,'message':'email already exist'})
		username = (first_name+''+last_name).title()
		if password==confirm_password:
			pwd = make_password(password)
			user_ins = User.objects.create(first_name=first_name,
											last_name=last_name,
											email=email,
											phonenumber=phonenumber,
											password=pwd,
											username=username,user_status=True)
			username=user_ins.username
			user_id= user_ins.pk
			user_ins.username=str(username)+str(user_id)

			created_by = user_ins.user_id
			user_ins.created_by = created_by
			user_ins.save()
			token = Token.objects.create(user=user_ins)
			user_id = User.objects.get(id=user_ins.id)                

			data = list(User.objects.filter(pk=user_ins.pk).values())

			# try:
			
			FROM_EMAIL = 'pendyalapradeepreddy0@gmail.com'
			To_Mail = user_ins.email

			subject = 'Welcome To Our Website'
			message = f'Hello {first_name},\n\n Thanks for register .We are Glad To have you with us!'
			Multiemail_notification(subject,message,To_Mail)
			# send_mail(subject, message, FROM_EMAIL, [To_Mail])
			# except:
			#   return JsonResponse({'success':False,'message':'mail not sent'})
			user_ids = Token.objects.get(key=token_key).user_id
			qs = list(User.objects.filter(id=user_id).values())

			qs1 = json.loads(json.dumps(qs,indent=4, sort_keys=True, default=str))


		else:
			return JsonResponse({'success':False,'message':'password did not match'})
		return JsonResponse({'success':True,'message':'successfully signup'})
	else:
		return JsonResponse({'success':False,'message':'methond not allowed'})
def authenticate(username= None,password=None):
	try:
		user= User.objects.get(email__iexact=username)
		if user.check_password(password):
			return user

	except User.DoesNotExist:
		return None

def Multiemail_notifications(subject,message,To_Mail):
	try:
		
		FROM_EMAIL = 'pendyalapradeepreddy0@gmail.com'
		send_mail(subject, message,FROM_EMAIL, [To_Mail])
	except:
		pass

def Multiemail_notification(subject,message,pdf_path,To_Mail):
	try:
		
		FROM_EMAIL = 'pendyalapradeepreddy0@gmail.com'
				
		email = EmailMultiAlternatives(subject, message, FROM_EMAIL, [To_Mail])
		email.attach_file(pdf_path)
		email.send()


	except Exception as e:
		print(f"Error sending email: {e}")


@csrf_exempt
@api_view(['POST'])

def login(request):
	if request.method == 'POST':
		email = request.data.get('email')
		password = request.data.get('password')
		if email and password:
			try:
				user_ins = User.objects.get(email__iexact=email)
			except:
				return JsonResponse({'success':False,'message':'such email not found'})
			user = authenticate(username=user_ins.email,password=password)
		if user:
			try:
				token= Token.objects.get(user__username= user.username)
			except:
				user_tk = User.objects.get(username=user.username)
				token = Token.objects.create(user=user_tk)
			
			# oder_header_details = {
				
			# 	"email" : user.email,
			# 	'username':user.username
			# }

			# context= {
			# 'order_details':oder_header_details
			# }
			template = get_template('newinvoice.html')
			html_string = template.render()
			pdf_path = os.path.join(settings.BASE_DIR, "media", f'invoice{user.pk}.pdf')
			pdfkit.from_string(html_string, pdf_path, options={'quiet': ''})
			if os.path.exists(pdf_path):
				download_link = request.build_absolute_uri(settings.MEDIA_URL + f'invoice{user.pk}.pdf')

			else:
				return "PDF generation failed"

			To_Mail = user.email
			subject = 'Your Loged in successfully'
			message = f'Hello {user.username}\n\n Welcome Back To Our Website'
			Multiemail_notification(subject,message,pdf_path,To_Mail)

			return JsonResponse({'success':True,'message':'login successful','pdf_download_link': download_link})
			
		else:
			return JsonResponse({'success':False,'token':token.key,'message':'inavalid password and email'})
	else:
		return JsonResponse({'success':False,'message':'method not allowed'})


@csrf_exempt
@api_view(['POST'])

def forgot_password(request):
	if request.method == 'POST':
		email = request.data.get('email')

		try:
			user_ins = User.objects.get(email__iexact=email)
		except:
			return JsonResponse({'success':False,'message':'email not exist '})

		if user_ins:
			otp = randint(1111,9999)
			try:
				user_ot = UserOtp.objects.get(user=user_ins)
				user_ot.user_otp=otp
				user_ot.save()
			except:
				otp_ins = UserOtp.objects.create(user=user_ins,user_otp= otp)

			To_Mail = user_ins.email
			subject = 'Otp Verification for login'
			message = f'Your verification opt is {otp} \n\n Thank You'
			Multiemail_notifications(subject,message,To_Mail)
			return JsonResponse({'success':True, 'message':'otp successfully sended'})

		else:
			return JsonResponse({'success':False,'message':'No user found'})
	else:
		return JsonResponse({'success':False,'message':'method not allowed'})

@csrf_exempt
@api_view(['POST'])

def verify_otp(request):
	if request.method=='POST':
		email = request.data.get('email')
		user_otp = request.data.get('user_otp')
		try:
			user_ins = User.objects.get(email__iexact=email)
		except:
			return JsonResponse({'success':False,'message':'email not found'})
		otp_ins = UserOtp.objects.get(user=user_ins)

		if otp_ins.user_otp == user_otp:
			return JsonResponse({'success':True,'message':'otp verified'})
		else:
			return JsonResponse({'success':False,'message':'inavlid Otp'})

@csrf_exempt
@api_view(['POST'])

def change_password(request):
	if request.method=='POST':
		email = request.data.get('email')
		user_otp = request.data.get('user_otp')
		new_password = request.data.get('new_password')
		try:
			user_ins = User.objects.get(email__iexact=email)
		except:
			return JsonResponse({'success':False,'message':'email not found'})
		try:
			otp_ins = UserOtp.objects.get(user=user_ins)
		except:
			return JsonResponse({'success':False,'message':'otp not found'})

		if otp_ins.user_otp== user_otp:
			user_ins.set_password(new_password)
			user_ins.save()
			To_Mail= user_ins.email
			subject = 'Password Changed successfully'
			message =f'Hello {user_ins.username} your password updated successfully'
			Multiemail_notification(subject,message,To_Mail)
			return JsonResponse({'success':True,'message':'password changed'})
		else:
			return JsonResponse({'success':False,'message':'otp mismatch'})
	else:
		return JsonResponse({'success':False,'message':'method not allowed'})

###############################################################################################
# @csrf_exempt
# @api_view(['GET'])

class BlogPostApi(APIView):
	permission_classes =[IsAllowedToWrite]
	def get(self,request):
		# if request.method == 'GET':

			data = list(BlogPost.objects.all().order_by('id').values())
			for i in data:
				i['blog_image'] = '/media/'+i['blog_image']
			return JsonResponse({'success':True,'data':data})
	def post(self,request):
		# if request.method == 'POST':
			# user_id = request.data.get('user_id')
			user_id = request.user.pk

			blog_title = request.data.get('blog_title')
			blog_image = request.data.get('blog_image')
			comment = request.data.get('comment')
			try:
				user_ins = User.objects.get(pk=user_id)

			except:
				return JsonResponse({'success':False})

			blog_ins= BlogPost.objects.create(user=user_ins,blog_title=blog_title,blog_image=blog_image,comment=comment,created_by=user_ins.user_id)

			data = list(BlogPost.objects.filter(id=blog_ins.id).values())
			for i in data:
				i['blog_image']='/media/'+i['blog_image']
			return JsonResponse({'success':True,'data':data})


	def put(self,request):

		# if request.method == 'PUT':
			blog_id= request.data.get('blog_id')

			blog_title = request.data.get('blog_title')
			blog_image = request.data.get('blog_image')
			comment = request.data.get('comment')
			try:
				blog_ins = BlogPost.objects.get(id=blog_id)
			except:
				return JsonResponse({'success':False,'message':'blog not found'})
			if not blog_title:
				blog_title=blog_ins.blog_title 
			if not blog_image:
				blog_image=blog_ins.blog_image 
			if not comment:
				comment=blog_ins.comment 
			BlogPost.objects.filter(id=blog_ins.id).update(blog_title=blog_title,blog_image=blog_image,comment=comment,modified_by=blog_ins.user.user_id)

			data = list(BlogPost.objects.filter(id=blog_ins.id).values())
			for i in data:
				i['blog_image']='/media/BlogImage/'+i['blog_image']
			return JsonResponse({'success':True,'data':data})


# @csrf_exempt
# @api_view(['POST'])

# def post_likes(request):
#   if request.method == 'POST':
#       post_id = request.data.get("post_id")
#       user_id = request.data.get('user_id')

#       try:
#           post_ins = BlogPost.objects.get(id=post_id)
#       except:
#           return JsonResponse({'success':False,'message':'post_id not found'})
#       try:
#           user_ins = User.objects.get(pk=user_id)
#       except:
#           return JsonResponse({'success':False,'message':'user_id not found'})
#       print(post_ins.like,'aaaaaaaaaaaaaaaaaa')

#       if BlogPost.objects.filter(user=user_ins).exists():
#           try:
#               if post_ins.like=='1' and user_ins==user_ins:
#                   post_ins.like=0
#                   post_ins.save()
#                   return JsonResponse({'success':True,'message':'like removed'})
#               # elif post_ins.like=='1' and user_ins!=user_ins:
#               #   post_ins.like+=1
#               #   post_ins.save()
#               #   return JsonResponse({'success':True,'message':'like increased'})
#               elif post_ins.like=='0' and user_ins==user_ins:
#                   post_ins.like=1
#                   post_ins.save()
#                   return JsonResponse({'success':True,'message':'like succes'})

#           except:
				
#               return JsonResponse({'success':False,'message':'inavlid'})

#       else:
#           return JsonResponse({'success':False})

@csrf_exempt
@api_view(['GET'])
def post_get(request):
	if request.method == 'GET':
		user_id = request.data.get('user_id')

		data = list(BlogPost.objects.filter(user=user_id).values())
		for i in data:
			i['blog_image']='/media/'+i['blog_image']

		return JsonResponse({'success':True,'data':data})
@csrf_exempt
@api_view(['POST'])

def like(request):
	if request.method =='POST':

		if request.user.is_anonymous:
		  return JsonResponse({'success': False, 'data': "token missing"})

		# user_id= request.data.get('user_id')
		post_id= request.data.get('post_id')
		try:
			post = BlogPost.objects.get(id=post_id)
		except:
			return JsonResponse({'success':False,'message':'post not found'})
		try:
			user_ins= User.objects.get(pk=request.user.pk)
		except:
			return JsonResponse({'success':False,'message':'user not found'})
		current_likes = post.like

		liked = Likes.objects.filter(user=user_ins, blogpost=post).count()
		if not liked:
			Likes.objects.create(user=user_ins, blogpost=post)
			current_likes = current_likes + 1
			post.like = current_likes
			post.save()
			return JsonResponse({'success':True,'message':'like added'})
		else:
			Likes.objects.filter(user=user_ins, blogpost=post).delete()
			if current_likes >0:
				current_likes = current_likes - 1
				post.like = current_likes
				post.save()
				return JsonResponse({'success':True,'message':'like removed'})
			else:
				current_likes =0
				post.like = current_likes
				post.save()
				return JsonResponse({'success':False,'message':'like are 0'})

@csrf_exempt
@api_view(['GET'])

def get_tokendetails(request):
	if request.method == 'GET':

		try:
			token_key = request.headers.get('Authorization').split()[1]
			token_ins = Token.objects.get(key=token_key)
		except:
			return JsonResponse({'success':False,'message':'invalid token'})

		user_ins = token_ins.user
	
		data = list(User.objects.filter(pk=user_ins.pk).values())
		return JsonResponse({'success':True,'data':data})

@csrf_exempt
@api_view(['GET'])

def single_get(request):
	if request.user.is_anonymous:
		  return JsonResponse({'success': False, 'data': "token missing"}) 
	user_ins = request.user
	if request.user.is_active:
		data = list(User.objects.filter(pk=user_ins.pk).values())
	else:
		return JsonResponse({'success':False})
	
	return JsonResponse({'success':True,'data':data})




class CourseCreateAllGetApi(APIView):

	def post(self, request):

		serializer = CourseSerializer(data= request.data)
		if serializer.is_valid():
			course_name = request.data.get('course_name')

			if (Course.objects.filter(course_name=course_name).exists()):
				return JsonResponse({'success':False,'message':'course already exist'})

			serializer.save()
			return JsonResponse({'success':True,'data':serializer.data})
	def get(self, request):
		data = Course.objects.all()
		serializer = CourseGetSerializer(data,many= True)
		return JsonResponse({'success':True,'data':serializer.data})

class CourseSingleGetUpdateDeleteApi(APIView):

	def get(self, request, id):
		try:
			task = Course.objects.get(pk=id)
		except:
			return JsonResponse({'success':False,'message':'id not found'})
		serializer = CourseGetSerializer(task)
		return JsonResponse({'success':True,'data':serializer.data})

	def put(self,request, id):
		try:
			task = Course.objects.get(pk=id)
		except:
			return JsonResponse({'success':False,'message':'id not found'})

		serializer = CourseGetSerializer(task, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse({'success':True,'data':serializer.data})

	def delete(self, request, id):
		try:
			task = Course.objects.get(pk=id)
			task.delete()
			return JsonResponse({'success':True,'message':'deleted successfully'})
		except:
			return JsonResponse({'success':False,'message':'id not found'})


class CouponCreateAllGetApi(APIView):

	def post(self, request):

		serializer = CouponSerializer(data= request.data)
		if serializer.is_valid():
			random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
			
			serializer.validated_data['coupon_code'] = random_string
			if (Coupon.objects.filter(coupon_code=random_string).exists()):
				return JsonResponse({'success':False,'message':'course already exist'})

			serializer.save()
			
			return JsonResponse({'success':True,'data':serializer.data})
		else:
			return JsonResponse({'success':False})
	def get(self, request):
		data = Coupon.objects.all()
		serializer = CouponGetSerializer(data,many= True)
		return JsonResponse({'success':True,'data':serializer.data})


class CouponSingleGetUpdateDeleteApi(APIView):
	def get(self, request, id):
		try:
			task = Coupon.objects.get(pk = id)
		except:
			return JsonResponse({'success':False,'message':'no id found'})
		serializer = CouponGetSerializer(task)
		return JsonResponse({'success':True,'data':serializer.data})

	def put(self, request, id):
		try:
			task = Coupon.objects.get(pk=id)
		except:
			return JsonResponse({'success':False,'message':'Not Found'})
		serializer = CouponSerializer(task, data= request.data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse({'success':True,'message':'updated successfully','data':serializer.data})
		else:
			return JsonResponse({'success':False,'message':'serializer errors'})

	def delete(self, request, id):
		try:
			task = Coupon.objects.get(pk=id)
			task.delete()
			return JsonResponse({'success':True,'message':'deleted successfully'})
		except:
			return JsonResponse({'success':False,'message':'not found'})

class StudentCreateAllGetApi(APIView):
	def post(self,request):

		serializer = StudentSerializer(data = request.data)
		course_id = request.data.get('course_id')
		student_name = request.data.get('student_name')
		if course_id:
			
			try:
				course_ins= ast.literal_eval(course_id)
			except:
				course_ins = json.dumps(course_id)
				course_ins = ast.literal_eval(course_ins)
				
				course = Course.objects.filter(pk__in=course_ins)
			if serializer.is_valid():
				if (Student.objects.filter(student_name=student_name).exists()):
					return JsonResponse({"success":False,'message':'already exist'})
				
				data= serializer.save()
				data.course_names.set(course_ins)
				return JsonResponse({'success':True,'message':'created successfully','data':serializer.data})


		if serializer.is_valid():
			if (Student.objects.filter(student_name=student_name).exists()):
				return JsonResponse({"success":False,'message':'already exist'})
			
			data= serializer.save()
			return JsonResponse({'success':True,'message':'created successfully','data':serializer.data})
		else:
			return JsonResponse({'success':False})

	def get(self,request):

		data = Student.objects.all().order_by('-id')
		serializer = StudentSerializer(data, many=True)
		return JsonResponse({'success':True,'data':serializer.data})

class StudentSingleGetUpdateDeleteApi(APIView):

	def get(self, request, id):
		try:
			task = Student.objects.get(id= id)
		except:
			return JsonResponse({'success':False,'message':'Id Not Found'})
		serializer = StudentSerializer(task)
		
		return JsonResponse({'success':True,'data':serializer.data})

	def put(self, request, id):
		try:
			task = Student.objects.get(id=id)
		except:
			return JsonResponse({'success':False,'message':'Id Not Found'})
		course_id = request.data.get('course_id')
		try:
			course_ins= ast.literal_eval(course_id)
		except:
			course_ins = json.dumps(course_id)
			course_ins = ast.literal_eval(course_ins)
	
		serializer = StudentSerializer(task,data= request.data)
		if serializer.is_valid():
			data= serializer.save()
			data.course_names.set(course_ins)

			return JsonResponse({'success':True,'data':serializer.data})
		else:
			return JsonResponse({'success':False})
	def delete(self, request, id):
		try:
			task = Student.objects.get(id=id)
			task.delete()
			return JsonResponse({'success':True,'message':'deleted successfully'})
		except:
			return JsonResponse({'success':False,'message':'Id Not Found'})

# class StundetRemoveCoursesApi(APIView):
#   def delete(self, request, id):
#       try:
#           task = Student.objects.get(id=id)
#       except:
#           return JsonResponse({'success':False,'message':'Id Not Found'})
#       course_id = request.data.get('course_id')
#       try:
#           course_ins= ast.literal_eval(course_id)
#       except:
#           course_ins = json.dumps(course_id)
#           course_ins = ast.literal_eval(course_ins)
#       for course_id in course_ins:
#           course = Course.objects.filter(pk=course_id).first()
#           # if (Student.objects.filter(course_names=))
#           if (Student.objects.filter(course_names=course).exclude(course_names=course).exists()):
#               return JsonResponse({'success':False,'message':'already exist'})
#           if course:
#               task.course_names.remove(course)
#           else:
#               return JsonResponse({'success': False, 'message': 'course id not found'})

#       serializer = StudentSerializer(task,data= request.data)
#       if serializer.is_valid():
#           data= serializer.save()
			
#           return JsonResponse({'success':True,'data':serializer.data})
#       else:
#           return JsonResponse({'success':False})



class PersonAllGetCreateApi(APIView):

	def post(self,request):
		serializer = PersonSerializer(data=request.data)
		name = request.data.get('name')

		if (Person.objects.filter(name=name).exists()):
			return JsonResponse({'success':False,'message':'name already exist'})

		if serializer.is_valid():
			serializer.save()
			return JsonResponse({'success':True,'message':serializer.data})
		else:
			return JsonResponse({'success':False,'message':'serializer noyt valid'})
	def get(self, request):
		data = Person.objects.all().order_by('-id')
		serializer= PersonSerializer(data,many=True)
		return JsonResponse({'success':True,'data':serializer.data})
class PersonSigleGetUpdateDelete(APIView):
	def get(self, request, id):
		try:
			task = Person.objects.get(id=id)
			serializer = PersonSerializer(task)
			return JsonResponse({'success':True,'data':serializer.data})
		except:
			return JsonResponse({'success':False,'message':'id not found'})
	def put(self, request,id):
		try:
			task = Person.objects.get(id=id)
		except:
			return JsonResponse({'success':False,'message':'id not found'})
		serializer = PersonSerializer(task, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse({'success':True,'data':serializer.data})
		else:
			return JsonResponse({'success':False,'message':serializer.errors})
	def delete(self, request, id):
		try:
			task = Person.objects.get(id=id)
			task.delete()
			return JsonResponse({'success':True,'data':'dleted successfully'})
		except:
			return JsonResponse({'success':False,'message':'id not found'})

class ProfileAllGetCreateApi(APIView):

	def post(self, request):

		serializer = ProfileSerializer(data=request.data,partial=True)

		name = request.data.get('person')

		try:
			person_ins= Person.objects.get(name=name)
		except:
			return JsonResponse({'success':False,'message':'person_id not exist'})

		if serializer.is_valid():
			profile_ins =serializer.save()
			profile_ins.person= person_ins
			profile_ins.save()
			return JsonResponse({'success':True,'message':serializer.data})
		else:
			return JsonResponse({'success':False,'errors':serializer.errors})

	def get(self, request):
		data = Profile.objects.all().order_by('-id')
		serializer = ProfileSerializer(data,many=True)
		return JsonResponse({'success':True,'data':serializer.data})

@csrf_exempt
@api_view(['GET'])
def user_followers(request):
	if request.method == 'GET':
		username = request.data.get('username')
		user = User.objects.get(username=username)
		followers_data =list(user.followers.all().values('follower'))
		return JsonResponse({'user': user.username, 'followers': followers_data})

class FollowAllGetAndCreateApi(APIView):
	def post(self, request):
		user_id = request.data.get('user_ids')
		user_ids = request.data.get('user_id')
		course_id = request.data.get('course_id')

		# if follower == following:
		# 	return JsonResponse({'success':False,'message':'user not follow himself'})
		# else:
		try:
			follower_ins = User.objects.get(pk=user_id)
		except:
			return JsonResponse({'success':False,'message':'user not found'})
		try:
			folloing_ins = User.objects.get(pk=user_ids)
		except:
			return JsonResponse({'success':False,'message':'user did not found'})

		try:
			convert_list = ast.literal_eval(course_id)
		except Exception:
			compo_li = json.dumps(course_id)
			convert_list = ast.literal_eval(compo_li)

		try:
			courses = Course.objects.filter(course_id__in=convert_list)
		except:
			return JsonResponse({'success':False,'message':'course errorr'})

		course_names = [course.course_name for course in courses]
		courses_string = ','.join(course_names)
		follow_ins = Follow.objects.create(follower=follower_ins,followed=folloing_ins,course=courses_string)

		follow_ins.save()
		return JsonResponse({'success':True,'message':'created successfully'})

	def get(self, request):
		data = Follow.objects.all().order_by('-pk')
		serializer = FollowGetSerializer(data,many=True)
		return JsonResponse({'success':True,'data':serializer.data})

class FollowSingleGetApi(APIView):
	def get(self,request):
		follow_id = request.data.get('follow_id')

		try:
			follow_ins = Follow.objects.get(id=follow_id)
		except:
			return JsonResponse({'success':False,'message':'id not found'})
		data = list(follow_ins.course)
		return JsonResponse({'success':True,'data':data})







###############################################################################

@api_view(['GET'])
@csrf_exempt
def all_order(request):
	if request.method=='GET':

		# payload={}

		api_url = 'https://apiv2.shiprocket.in/v1/external/orders'
		headers = {
			'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQ2NTgxMzIsInNvdXJjZSI6InNyLWF1dGgtaW50IiwiZXhwIjoxNzE1MDYzNjMzLCJqdGkiOiJZZUFNaFdFaEtnYU9JaENHIiwiaWF0IjoxNzE0MTk5NjMzLCJpc3MiOiJodHRwczovL3NyLWF1dGguc2hpcHJvY2tldC5pbi9hdXRob3JpemUvdXNlciIsIm5iZiI6MTcxNDE5OTYzMywiY2lkIjo0MzExNzI5LCJ0YyI6MzYwLCJ2ZXJib3NlIjpmYWxzZSwidmVuZG9yX2lkIjowLCJ2ZW5kb3JfY29kZSI6IiJ9.r-tTJchvmvbBIc0XSlx9X48nFbUMO_p5ssDkOxSebyg',
			'Content-Type' : 'application/json'
		}
		response = requests.get(api_url, headers=headers)
	
		data = response.json()

		return JsonResponse({'success':True,'data':data })


@api_view(['GET'])
@csrf_exempt
def track_order(request):
	if request.method=='GET':

		shipment_id = request.data.get('shipment_id')
		api_url = f"https://apiv2.shiprocket.in/v1/external/shipments/{shipment_id}"
		headers = {
			'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQ2NTgxMzIsInNvdXJjZSI6InNyLWF1dGgtaW50IiwiZXhwIjoxNzE1MDYzNjMzLCJqdGkiOiJZZUFNaFdFaEtnYU9JaENHIiwiaWF0IjoxNzE0MTk5NjMzLCJpc3MiOiJodHRwczovL3NyLWF1dGguc2hpcHJvY2tldC5pbi9hdXRob3JpemUvdXNlciIsIm5iZiI6MTcxNDE5OTYzMywiY2lkIjo0MzExNzI5LCJ0YyI6MzYwLCJ2ZXJib3NlIjpmYWxzZSwidmVuZG9yX2lkIjowLCJ2ZW5kb3JfY29kZSI6IiJ9.r-tTJchvmvbBIc0XSlx9X48nFbUMO_p5ssDkOxSebyg',
			'Content-Type' : 'application/json'
		}
		response = requests.get(api_url, headers=headers)
		data = response.json()

		return JsonResponse({'success':True,'data':data })

@api_view(['POST'])
@csrf_exempt
def create_order(request):

	if request.method == "POST":

		payload = json.dumps({
		  "order_id": "86887146",
		  "order_date": "2024-05-06 11:30",
		  "pickup_location": "villa",
		  # "channel_id": "",
		  # "comment": "Reseller: M/s Goku",
		  "billing_customer_name": "pradeep",
		  "billing_last_name": "P",
		  "billing_address": "1-104, warangal",
		  # "billing_address_2": "Near Hokage House",
		  "billing_city": "Warangal",
		  "billing_pincode": "506001",
		  "billing_state": "Telangana",
		  "billing_country": "India",
		  "billing_email": "pradeepreddyp1999@gmail.com",
		  "billing_phone": "8655654552",
		  "shipping_is_billing": True,
		  "shipping_customer_name": "",
		  # "shipping_last_name": "",
		  "shipping_address": "",
		  # "shipping_address_2": "",
		  "shipping_city": "",
		  "shipping_pincode": "",
		  "shipping_country": "",
		  "shipping_state": "",
		  # "shipping_email": "",
		  "shipping_phone": "",
		  "order_items": [
		    {
		      "name": "current affairs",
		      "sku": "chakra123",
		      "units": 10,
		      "selling_price": "900",
		      # "discount": "",
		      # "tax": "",
		      # "hsn": 441122
		    }
		  ],
		  "payment_method": "Prepaid",
		  # "shipping_charges": 0,
		  # "giftwrap_charges": 0,
		  # "transaction_charges": 0,
		  # "total_discount": 0,
		  "sub_total": 9000,
		  "length": 10,
		  "breadth": 15,
		  "height": 20,
		  "weight": 2.5
		})

		api_url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
		
		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQ2NTgxMzIsInNvdXJjZSI6InNyLWF1dGgtaW50IiwiZXhwIjoxNzE1MDYzNjMzLCJqdGkiOiJZZUFNaFdFaEtnYU9JaENHIiwiaWF0IjoxNzE0MTk5NjMzLCJpc3MiOiJodHRwczovL3NyLWF1dGguc2hpcHJvY2tldC5pbi9hdXRob3JpemUvdXNlciIsIm5iZiI6MTcxNDE5OTYzMywiY2lkIjo0MzExNzI5LCJ0YyI6MzYwLCJ2ZXJib3NlIjpmYWxzZSwidmVuZG9yX2lkIjowLCJ2ZW5kb3JfY29kZSI6IiJ9.r-tTJchvmvbBIc0XSlx9X48nFbUMO_p5ssDkOxSebyg'
		}

		response = requests.request('POST',api_url, headers=headers, data=payload)

		data = response.json()

		return JsonResponse({'success':True,'data':data })

import pandas as pd

from django.utils import timezone
@csrf_exempt
@api_view(['POST'])
def export_data_to_excel(request):
    if request.method == 'POST':
        # Get all User objects from the database
        users = User.objects.all()
        print("Number of users fetched:", users.count())
        # Convert timezone-aware datetimes to timezone-unaware datetimes
        user_data = []
        for user in users:
            # Convert timezone-aware datetimes to timezone-unaware datetimes
            if user.date_joined.tzinfo is not None:
                date_joined = user.date_joined.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                date_joined = user.date_joined

            user_data.append({
                'Username': user.username,
                'Email': user.email,
                'First Name': user.first_name,
                'Last Name': user.last_name,
                'Date Joined': date_joined,  # Use timezone-unaware datetime
            })

        # Create a DataFrame from the User objects
        user_df = pd.DataFrame(user_data)
        print("First few rows of DataFrame:")
        print(user_df.head())

        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter('output_data.xlsx', engine='xlsxwriter')

        # Write the DataFrame to a worksheet
        user_df.to_excel(writer, sheet_name='Users', index=False)

        # Close the Pandas Excel writer to save the Excel file
        writer.close()

        return JsonResponse({'success': True, 'message': 'Data exported to Excel successfully'})

    else:
    	return JsonResponse({'success':False})


class ProductCreationApi(APIView):
	def post(self,request):

		serializer = ProductSerializer(data =request.data)

		if serializer.is_valid():
			serializer.save()
			return JsonResponse({'success':True,'data':serializer.data})
		else:
			return JsonResponse({'success':False,'error':serializer.errors})
import logging
from django.http import HttpResponse
logger = logging.getLogger(__name__)
class TestLoger(APIView):
	def get(self, request):
	    # raise Exception("This is a test exception!")
	    # print(data)
	    # return HttpResponse("This should never be reached.")
	    # # try:
	    # #     print(hjdgu)
	    # # except Exception as e:
	    # #     logger.error('An error occurred: %s', e, exc_info=True)
	    # #     return JsonResponse({"success": False, "message": str(
	    # #             e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


	    try:
	        # Code that may raise an exception
	        raise Exception("This is a test exception!")
	    except Exception as e:
	        # Log the exception with full traceback
	        logger.error('An error occurred: %s', e, exc_info=True)
	        # Return an error response
	        return JsonResponse({"error": str(e)}, status=500)