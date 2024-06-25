from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	username = models.CharField(max_length=100, blank=True, null=True, unique=True)
	email = models.EmailField()
	phonenumber = models.IntegerField(null=True,blank=True,unique=True)
	password = models.CharField(max_length=100,blank=True, null= True)
class Product(models.Model):
	product_name = models.CharField(max_length=100, blank=True, null=True)
	product_cost = models.CharField(max_length=100,default=0.0, blank=True, null=True)
	

class UserWishlist(models.Model):
	product = models.ManyToManyField(Product,blank=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)