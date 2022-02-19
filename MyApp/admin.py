from django.contrib import admin

# Register your models here.
from MyApp.models import User, FriendRequest

admin.site.register(User)
admin.site.register(FriendRequest)
