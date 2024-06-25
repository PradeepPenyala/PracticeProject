from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Timebasedmodel(models.Model):
	created_on = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	modified_on = models.DateTimeField(auto_now=True,blank=True,null=True)

	class Meta:
		abstract = True

class User(AbstractUser,Timebasedmodel):
	user_id = models.BigAutoField(primary_key= True,editable= False)
	first_name = models.CharField(max_length=100,blank=True, null=True)
	last_name = models.CharField(max_length=100,blank= True,null= True)
	email = models.EmailField()
	phonenumber = models.CharField(max_length=100, null= True, blank=True, unique=True)
	password = models.CharField(max_length=100,blank=True,null=True)
	username = models.TextField(max_length=100,blank=True,null=True,unique=True)
	user_status = models.BooleanField(default=False)
	created_by = models.CharField(max_length=100,blank=True,null=True)
	modified_by= models.CharField(max_length=100,blank=True,null=True)


class UserOtp(Timebasedmodel):
	user_otp = models.CharField(max_length=100, null=True,blank=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

class BlogPost(Timebasedmodel):
	blog_title = models.CharField(max_length=250,blank=True,null=True)
	blog_image = models.ImageField(upload_to= 'BlogImage',blank=True,null=True)
	comment = models.CharField(max_length=256,blank=True,null=True)
	like= models.IntegerField(blank=True,null=True,default=0)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null= True,blank=True)
	created_by = models.CharField(max_length=100,blank=True,null=True)
	modified_by= models.CharField(max_length=100,blank=True,null=True)

class Likes(Timebasedmodel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	blogpost = models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='post_likes')

class Course(Timebasedmodel):
	course_id = models.AutoField(primary_key=True,editable=False)
	course_name = models.CharField(max_length=100,blank=True,null=True)
	course_price =models.IntegerField(default=0.0,blank=True,null=True)


class Coupon(Timebasedmodel):
	coupon_id = models.AutoField(primary_key=True,editable=False)
	coupon_code = models.TextField(max_length=100,blank=True,null=True)
	discount_amount = models.IntegerField(blank= True,null=True)

class Student(Timebasedmodel):
	student_name = models.CharField(max_length=100,blank=True,null=True)
	course_names = models.ManyToManyField(Course,blank=True)

class Person(Timebasedmodel):
	name = models.CharField(max_length=100,blank=True,null=True)

class Profile(Timebasedmodel):
	person = models.OneToOneField(Person,on_delete = models.CASCADE)
	bio = models.TextField(max_length=200,blank=True,null=True)
	email = models.EmailField()


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.TextField(max_length=200,null=True,blank=True)



class Product(models.Model):
	product_name = models.CharField(max_length=100, null=True, blank=True)
	product_type = models.CharField(max_length=100,blank=True,null=True)
	product_price = models.IntegerField(default=0.0)
	quality = models.CharField(max_length=100,blank=False,null=False)
