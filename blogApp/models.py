from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from asyncio.windows_events import NULL
from datetime import datetime
from tkinter import CASCADE
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from hitcount.models import HitCountMixin, HitCount

CATEGORIES = (
    ("ravan" ,"رشد فردی"),
    ("iran","ادبیات ایران"),
    ("russ","ادبیات روس"),
    ("eng","ادبیات انگلیسی"),
    ("france","ادبیات فرانسه")
)
class Category(models.Model):
     name = models.CharField(max_length=250, unique=True)
class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='images',null=True,blank=True)
    lastModified = models.DateTimeField(auto_now=True)
    publishDate = models.DateTimeField(auto_now_add=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', 
                                        related_query_name='hit_count_generic_relation')
    comments = GenericRelation(Comment)
    category = models.CharField(max_length=1000, choices=CATEGORIES ,null=True,blank=True)
    
    def get_related_posts_by_tags(self):
           return Post.objects.filter(category=self.category).exclude(pk=self.pk)
    


    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)
