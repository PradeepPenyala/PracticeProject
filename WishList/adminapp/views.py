from django.shortcuts import render
from adminapp.models import User,Product,UserWishlist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
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
@api_view(['POST'])
@csrf_exempt
def register(request):
	if request.method == 'POST':
		first_name= request.data.get('first_name')
		last_name = request.data.get('last_name')
		email = request.data.get('email')
		phonenumber = request.data.get('phonenumber')
		password = request.data.get('password') 
		confirm_password = request.data.get('confirm_password')
		if not first_name.isalpha():
				return JsonResponse({'error': 'First name must contain only alphabetic characters'})
		if not last_name.isalpha():
				return JsonResponse({'error': 'Last name must contain only alphabetic characters'})
		email = email.lower()
		if not email or not password or not first_name or not last_name:
			return JsonResponse ({'error':'please provide all fields'})
			
		if User.objects.filter(email__iexact=email).exists():
			return JsonResponse({'error':'email already exist try another'})

		
		username=(first_name+''+last_name).title()  
		if password==confirm_password:
			pwd=make_password(password)
			user_ins = User.objects.create(first_name=first_name,
											last_name=last_name,
											username=username,
											phonenumber=phonenumber,
											email=email,password=pwd)
			username = user_ins.username
			user_id = user_ins.id
			user_ins.username = str(username) + str(user_id)

			user_ins.save()

			token = Token.objects.create(user = user_ins)
			data = list(User.objects.filter(id = user_ins.id).values())
			try:
				To_Mail = user_ins.email
				FROM_EMAIL = 'pendyalapradeepreddy0@gmail.com'
				subject = 'Welcome to Our Site!'
				message = f'Hello {first_name},\n\nWelcome to our site. We are glad to have you with us!'
				send_mail(subject, message, FROM_EMAIL, [To_Mail])
			except:
				
				return JsonResponse({'error': 'An error occurred while sending the welcome email'})
		
		else:
			return JsonResponse({'inavlid':'password missmatch'})
	return JsonResponse({'success': True, 'created user': "User Created Successfully.",'token':token.key})

def authenticate(username=None, password=None):

	try:
		user = User.objects.get(email__iexact=username)
		if user.check_password(password):
			return user
	except User.DoesNotExist:
		return None


@api_view(['POST'])
@csrf_exempt
def login(request):
	email = request.data.get('email')
	password = request.data.get('password')
	if email and password:
		
		try:
			user_ins=User.objects.get(email__iexact=email)
			
		except Exception:
			return JsonResponse({"success": False,"data": "wrong email"},)

		user = authenticate(username=user_ins.email, password=password)

		if user:
			
			try:
				token = Token.objects.get(user__username=user.username)
			except Token.DoesNotExist:
				user_qs = User.objects.get(username=user.username)
				token = Token.objects.create(user=user_qs)
			To_Mail = user.email
			subject = 'Login Notification'
			message = f'Hello {user.username},\n\n Welcome Back in to our website.'
			Multiemail_notification(subject,message,To_Mail)
			data = list(User.objects.filter(id=user.id).values())

			return JsonResponse({"success": True,"token": token.key,"login user": 'successfully loged in Welcome back '})

		else:
			return JsonResponse({"success": False,"data": " user not found"})
	 
	else:
		return JsonResponse({"success": False,"data": "Enter Valid Email and Password"})
@api_view(['PUT'])
@csrf_exempt
def edit_user(request):
	if request.method == 'PUT':
		email = request.data.get('email')
		password = request.data.get('password')
		first_name= request.data.get('first_name')
		last_name = request.data.get('last_name')
		phonenumber = request.data.get('phonenumber')
		try:
			user_ins= User.objects.get(email__iexact=email)
		except:
			return JsonResponse({'not found':'email id not found'})
		user = authenticate(username=user_ins.email, password=password)
	
		if user:

			user_ins = User.objects.filter(id=user_ins.id).update(first_name=first_name,
																	last_name=last_name,
																	phonenumber=phonenumber)
			
			return JsonResponse({'success':True,'updates':'user details updated'})
		else:
			return JsonResponse({'success':False,'error':'no user found'})


########################################################################

@api_view(['POST'])
@csrf_exempt
def create_prod(request):
	if request.method == 'POST':
		product_name = request.data.get('product_name')
		product_cost = request.data.get('product_cost')
		if not product_name or not product_cost:
			return JsonResponse ({'error':'please provide all fields'})
		else:
			product_ins = Product.objects.create(product_name=product_name,
													product_cost=product_cost)
			data = list(Product.objects.filter(id=product_ins.id).values())
			return JsonResponse({'success':True,'data':data})
@api_view(['GET'])
@csrf_exempt
def read_prod(request):
	if request.method == 'GET':
		product_id = request.data.get('product_id')
		try:
			product_ins = Product.objects.get(id=product_id)
		except:
			return JsonResponse({'invalid':'id not found'})
		data = list(Product.objects.filter(id=product_ins.id).values())
		return JsonResponse({'success':True,'data':data})

@api_view(['PUT'])
@csrf_exempt
def update_prod(request):
	if request.method == 'PUT':
		product_id = request.data.get('product_id')
		product_name = request.data.get('product_name')
		product_cost = request.data.get('product_cost')
		try:
			product_ins = Product.objects.get(id=product_id)
		except:
			return JsonResponse({'not found':'no id found'})
		if product_name:
			product_ins.product_name = product_name
		if product_cost:
			product_ins.product_cost = product_cost
		if product_ins:

			Product.objects.filter(id=product_ins.id).update(product_name=product_name,
																product_cost=product_cost)
			product_ins.save()
			data = list(Product.objects.filter(id=product_ins.id).values())
			return JsonResponse({'success':True,'data':data})
		else:
			return JsonResponse({'success':False,'error':'no id found'})

	else:
		return JsonResponse({'success':False,'error':'select correct method'})

@api_view(['DELETE'])
@csrf_exempt
def delete_prod(request):
	if request.method == 'DELETE':
		product_id = request.data.get('product_id')
		try:
			product_ins = Product.objects.get(id=product_id).delete()
		except:
			return JsonResponse({'Not Found':'id not found'})
		return JsonResponse({'success':True,'data':'id deleted successfully'})

@api_view(['POST'])
@csrf_exempt
def create_wishlist(request):
	if request.method == 'POST':
		email = request.data.get('email')
		product_id = request.data.get('product_id')
		try:
			user = User.objects.get(email__iexact=email)
		except:
			return JsonResponse({'success':False,'message':'no user id found'})
		try:
			product= Product.objects.get(id=product_id)
		except:
			return JsonResponse({'success':True,'message':'no product id found'})
		
		wishlist, created = UserWishlist.objects.get_or_create(user=user)

		wishlist.product.add(product)
		data = list(UserWishlist.objects.filter(id=wishlist.id).values())

		return JsonResponse({'success':True,'message':'product added to wishlist'})

@api_view(['GET'])
@csrf_exempt
def read_wishlist(request):
	if request.method == 'GET':
		wishlist_id = request.data.get('wishlist_id')
		try:
			wishlist_ins = UserWishlist.objects.get(id= wishlist_id)
		except:
			return JsonResponse({'success':False,'message':'id not found'})

		results = list(UserWishlist.objects.filter(id=wishlist_ins.id).values())
		for i in results:
			i['user_id'] = list(User.objects.filter(id=i['user_id']).values())
			for j in i['user_id']:
				j['id'] = list(wishlist_ins.product.values())

		return JsonResponse({'success':True,'message':results})

@api_view(['DELETE'])
@csrf_exempt
def delete_wishlistprod(request):
	if request.method == 'DELETE':
		wishlist_id = request.data.get('wishlist_id')
		product_id = request.data.get('product_id')
		try:
			wishlist_ins= UserWishlist.objects.get(id=wishlist_id)
		except:
			return JsonResponse({'success':False,'message':'not found'})
		try:
			product_ins = Product.objects.get(id=product_id)
		except:
			return JsonResponse({'success':False,'message':'product id not found'})
		wishlist_ins.product.remove(product_ins)
		return JsonResponse({'success':True,'message':'product deleted successfully'})


@api_view(['PUT'])
@csrf_exempt
def update_wishlist(request):
	if request.method == 'PUT':
		product_id = request.data.get('product_id')

		wishlist_id = request.data.get('wishlist_id')
		try:
			wishlist_ins = UserWishlist.objects.get(id=wishlist_id)
		except:
			return JsonResponse({'success':False,'message':'no id found'})
		try:
			product_ins= Product.objects.get(id=product_id)
		except:
			return JsonResponse({'success':False,'message':'no product id found'})
		wishlist_ins.product.add(product_ins)
		return JsonResponse({'success':True,'message':'product added successfully'})


