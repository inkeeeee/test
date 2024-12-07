from django.db import models
from django.contrib.auth.models import User
from .resources import *

class Author(models.Model):
    rating = models.IntegerField(default=0)    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def update_rating(self):
        post_rating = 0
        comm_author_rating = 0
        comm_post_rating = 0
        for post in Post.objects.filter(author=self):
            post_rating += post.rating
        for comm_author in Comment.objects.filter(user=self.user):
            comm_author_rating += comm_author.rating

        for comm_post in filter(lambda comm: comm.post.author==self, Comment.objects.all()):
            comm_post_rating += comm_post.rating

        self.rating = 3 * post_rating + comm_post_rating + comm_author_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
 
class Post(models.Model):
    kind = models.CharField(max_length=7, choices=KINDS, default=news)
    time_in = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='tittle')
    text = models.TextField(default='пустой пост')
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return str(self.text)[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='пустой комментарий')
    time_in = models.DateTimeField(auto_now_add = True)

    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()
