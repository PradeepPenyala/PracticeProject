from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('edit_user',views.edit_user,name='edit_user'),
    path('create_prod',views.create_prod,name='create_prod'),
    path('read_prod',views.read_prod,name='read_prod'),
    path('update_prod',views.update_prod,name='update_prod'),
    path('create_wishlist',views.create_wishlist,name='create_wishlist'),
    path('read_wishlist',views.read_wishlist,name='read_wishlist'),
    path('delete_wishlistprod',views.delete_wishlistprod,name='delete_wishlistprod'),
    path('update_wishlist',views.update_wishlist,name='update_wishlist'),
    ]