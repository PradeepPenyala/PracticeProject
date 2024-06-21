from django.contrib import admin

# Register your models here.
from adminapp.models import User,Customer,UserToken,CustomerToken
admin.site.register([User, Customer,UserToken,CustomerToken])

