from django.db import models
from django.contrib.auth import get_user_model

import datetime
User=get_user_model()

class MyFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    a_file = models.FileField(upload_to='files',)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    can_see = models.ManyToManyField(User,related_name='file')
    publish_comment=models.BooleanField(default=False)
    share_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description

class Comment(models.Model):
    reply = models.TextField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    file_obj=models.ForeignKey(MyFile,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.reply


