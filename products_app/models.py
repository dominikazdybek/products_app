from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=64)
    description = models.TextField()

    @property
    def quantity_of_likes(self):
        return self.likedislike_set.filter(liked=True).count()

    @property
    def quantity_of_dislikes(self):
        return self.likedislike_set.filter(liked=False).count()

    @property
    def quantity_of_comments(self):
         return self.comment_set.count()

    @property
    def likes(self):
            return self.likedislike_set.filter(liked=True)

    @property
    def dislikes(self):
        return self.likedislike_set.filter(liked=False)


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    product = models.ForeignKey(Product)


class LikeDislike(models.Model):
    liked = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    product = models.ForeignKey(Product)

