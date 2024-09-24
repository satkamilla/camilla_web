from django.contrib import admin

from .models import Master, Client, CustomUser
admin.site.register(Master) 
admin.site.register(Client)
admin.site.register(CustomUser)