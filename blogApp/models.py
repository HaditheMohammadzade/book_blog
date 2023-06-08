from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='images',null=True,blank=True)
    lastModified = models.DateTimeField(auto_now=True)
    publishDate = models.DateTimeField(auto_now_add=True)
