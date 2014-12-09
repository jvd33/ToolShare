from django.contrib import admin
from userManagement.models import ourUser, FeedBack

# Register your models here.
admin.site.register(ourUser)
admin.site.register(FeedBack)