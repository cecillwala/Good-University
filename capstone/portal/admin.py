from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import *
# Register your models here.

admin.site.register(User)
