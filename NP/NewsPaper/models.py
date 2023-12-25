from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        pc_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']

        self.rating = posts_rating * 3 + comments_rating + pc_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    news = 'NE'
    article = 'AR'
    TYPES = [(news, 'Новость'), (article, 'Статья')]

    type = models.TextField(max_length=2, choices=TYPES, default=news)
    title = models.CharField(max_length=255)
    text = models.TextField()
    time_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) >= 124:
            return self.text[:124] + '...'
        else:
            return self.text


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.CharField(max_length=255)
    time_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

