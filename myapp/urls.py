from django.contrib import admin
from django.urls import path
from .import views
# from .views import test_error

urlpatterns = [
		path('signup',views.signup,name='signup'),
		path('login',views.login,name='login'),
		path('forgot_password',views.forgot_password,name='forgot_password'),
		path('verify_otp',views.verify_otp,name='verify_otp'),
		path('change_password',views.change_password,name='change_password'),
		# path('blog_post',views.blog_post,name='blog_post'),
		# path('post_allget',views.post_allget,name='post_allget'),
		# path('post_likes',views.post_likes,name='post_likes'),
		path('BlogPostApi',views.BlogPostApi.as_view(),name='BlogPostApi'),
		path('post_get',views.post_get,name='post_get'),
		path('like',views.like,name='like'),
		# path('blog_post_update',views.blog_post_update,name='blog_post_update'),
		path('get_tokendetails',views.get_tokendetails,name='get_tokendetails'),
		path('single_get',views.single_get,name='single_get'),
		path('cource',views.CourseCreateAllGetApi.as_view(),name='create-course'),
		path('single_get/<int:id>',views.CourseSingleGetUpdateDeleteApi.as_view(),name='single-get-course-details'),
		path('coupon',views.CouponCreateAllGetApi.as_view(),name='create-allget-coupon'),
		path('get_update_delete_coopon/<int:id>',views.CouponSingleGetUpdateDeleteApi.as_view(),name='singleget-update-delete-coupon'),
		path('student',views.StudentCreateAllGetApi.as_view(),name='create-allget-student'),
		path('student_update_delete_retrive/<int:id>',views.StudentSingleGetUpdateDeleteApi.as_view(),name='singleget-update-delete-student'),
		# path('student_remove/<int:id>',views.StundetRemoveCoursesApi.as_view(),name='remove-course-from-student'),
		path('person',views.PersonAllGetCreateApi.as_view(),name='all-get-create-person'),
		path('v1/person/<int:id>',views.PersonSigleGetUpdateDelete.as_view(),name='single-get-update-delete-person'),
		path('profile',views.ProfileAllGetCreateApi.as_view(),name='all-get-create-profile'),
		path('user_followers',views.user_followers,name='user_followers'),
		path('FollowAllGetAndCreateApi',views.FollowAllGetAndCreateApi.as_view(),name='FollowAllGetAndCreateApi'),
		path('FollowSingleGetApi',views.FollowSingleGetApi.as_view(),name='FollowSingleGetApi'),
		path('track_order',views.track_order,name='track_order'),
		path('all_order',views.all_order,name='all_order'),
		path('create_order',views.create_order,name='create_order'),
		path('export_data_to_excel',views.export_data_to_excel,name='export_data_to_excel'),
		path('ProductCreationApi',views.ProductCreationApi.as_view(),name='product-create'),
		path('test-error/', views.TestLoger.as_view(), name='test_error'),

		]