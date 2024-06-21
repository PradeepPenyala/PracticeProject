from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from .managers import ActiveProductManager

class User(AbstractUser):
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	username = models.CharField(max_length=100, blank=True, null=True, unique=True)
	email = models.EmailField()
	phonenumber = models.IntegerField(null=True,blank=True,unique=True)
	password = models.CharField(max_length=100,blank=True, null= True)

class Faqs(models.Model):
	question = models.TextField(max_length=250,null= True,blank=True)
	answer = models.TextField(max_length=250,null= True,blank=True)

class Product(models.Model):
	product_name = models.CharField(max_length=100, blank=True, null=True)
	product_price = models.FloatField(default=0.0)
	status = models.BooleanField(default=False)

	objects = ActiveProductManager()