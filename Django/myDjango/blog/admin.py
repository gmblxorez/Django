from django.contrib import admin
from .models import Blog, Comment
from django.contrib.auth.models import Permission

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Permission)