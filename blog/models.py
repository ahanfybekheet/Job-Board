from ast import keyword
from django.db import models
from django.contrib.auth.models import User
from accounts.models import profile
from slugify import slugify

class Blog(models.Model):
    author = models.ForeignKey(profile, related_name="user_blog", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    about = models.CharField(max_length=500)
    article = models.TextField()
    category = models.ForeignKey("Category",related_name="blog_category",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    keyword = models.ManyToManyField("Keyword",related_name="keyword_blog")
    pub_at = models.DateField(auto_now_add=True)
    mod_at = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True,blank=True,null=True)


    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog,self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Keyword(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Comment(models.Model):
    owner = models.ForeignKey(profile,related_name="user_comment",on_delete=models.CASCADE)
    post = models.ForeignKey("Blog",related_name="blog_comment",on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    pub_at  = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment