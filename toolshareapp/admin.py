from django.contrib import admin
from toolshareapp.models import Tool, Shed, Community, Reservation, Statistics


# Register your models here.
admin.site.register(Tool)
admin.site.register(Shed)
admin.site.register(Community)
admin.site.register(Reservation)
admin.site.register(Statistics)