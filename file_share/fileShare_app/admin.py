from django.contrib import admin
from .models import MyFile,Comment
# Register your models here.
admin.site.register(MyFile)
admin.site.register(Comment)