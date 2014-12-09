from django.contrib import admin
from messageBoard.models import communityWall, Post

# Registered models appear on the admin page, when logged in as admin:
admin.site.register(communityWall)
admin.site.register(Post)
