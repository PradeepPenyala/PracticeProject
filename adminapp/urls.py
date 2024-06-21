from django.contrib import admin
from django.urls import path
from adminapp import views

urlpatterns = [
    path('CreateUser',views.CreateUser.as_view(),name = 'CreateUser'),
    path('CreateCustomer',views.CreateCustomer.as_view(),name='CreateCustomer'),
    path('CustomerGet',views.CustomerGet.as_view(),name='CustomerGet'),
]
