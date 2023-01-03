from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

article = 'AR'
news = "NW"

OPTIONS = [
    (article, 'статья'),
    (news, "новость")
]



class Author(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)


    def __str__(self):
        return f'{self.name}'

    def update_rating(self):
        self.rating = 0
        for comm in Comment.objects.filter(user=self.user):
            self.rating += comm.rate_comment
        for post in Posts.objects.filter(authors=Author.objects.get(user=self.user)):
            self.rating += post.rate_post * 3
            for comm_post in Comment.objects.filter(posts=post):
                self.rating += comm_post.rate_comment
        self.save()


class Category(models.Model):
    name = models.CharField(max_length = 30, unique = True)

class Posts(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    option = models.CharField(max_length = 2,
                              choices = OPTIONS,
                              default = news)
    dt_of_publication = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 150)
    text = models.CharField(max_length = 10000)
    rate_post = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through = 'PostCategory')


    @property
    def post_rating(self):
        return self.rate_post

    @post_rating.setter
    def post_rating(self, value):
        if value >= 0 and isinstance(value, int):
            self.rate_post = value
        else:
            self.rate_post = 0
        self.save()

    def like(self):
        self.rate_post += 1
        self.save()

    def dislike(self):
        self.rate_post -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'Заголовок: {self.title}, Текст: {self.text[:20]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length = 1000)
    dt = models.DateTimeField(auto_now_add = True)
    rate_comment = models.IntegerField(default=0)

    @property
    def rate_com(self):
        return self.rate_comment

    @rate_com.setter
    def rate_com(self, value):
        if value >= 0 and isinstance(value, int):
            self.rate_comment = value
        else:
            self.rate_comment = 0
        self.save()

    def __str__(self):
        return self.text

    def like(self):
        self.rate_comment += 1
        self.save()

    def dislike(self):
        self.rate_comment -= 1
        self.save()

class SubscribersUsers(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ForeignKey('Category', on_delete=models.CASCADE)