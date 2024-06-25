from django.contrib import admin

from adminapp.models import User,Product,UserWishlist

admin.site.register(User)
admin.site.register(Product)
admin.site.register(UserWishlist)