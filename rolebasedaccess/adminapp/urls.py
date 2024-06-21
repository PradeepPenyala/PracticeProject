from django.contrib import admin
from django.urls import path
from adminapp import views

urlpatterns = [
    path('GroupCreteApi',views.GroupCreteApi.as_view(),name='GroupCreteApi'),
    path('AllGetGroup',views.AllGetGroup.as_view(),name='AllGetGroup'),
    path('AllGetPermissions',views.AllGetPermissions.as_view(),name='AllGetPermissions'),
    path('AddPermissionsToRole',views.AddPermissionsToRole.as_view(),name='AddPermissionsToRole'),
    path('FaqsCreateApi',views.FaqsCreateApi.as_view(),name='FaqsCreateApi'),
    path('AllGetFaqs',views.AllGetFaqs.as_view(),name='AllGetFaqs'),
    path('UpdatePermissionsToRole',views.UpdatePermissionsToRole.as_view(),name='UpdatePermissionsToRole'),
    path('AddingGroupToUser',views.AddingGroupToUser.as_view(),name='AddingGroupToUser'),
    path('AllgetUser',views.AllgetUser.as_view(),name='AllgetUser'),

    path('ProductGet',views.ProductGet.as_view(),name='ProductGet'),
    
]
