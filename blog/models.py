from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import time
from django.contrib import admin
# from django_markdown.widgets import MarkdownWidget


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=70, blank=True, null=True)
    like = models.IntegerField(default=50)
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True)

    about_me = models.TextField(max_length=120, blank=True, null=True)

    pGitHub = models.CharField('GitHub', max_length=100, blank=True, null=True)
    pLinkedIn = models.CharField('LinkedIn', max_length=100, blank=True, null=True)
    pReplace = models.CharField('Replace.org.ua', max_length=100, blank=True, null=True)
    pCodeguida = models.CharField('Codeguida', max_length=100, blank=True, null=True)
    pFacebook = models.CharField('Facebook', max_length=100, blank=True, null=True)
    pTwitter = models.CharField('Twitter', max_length=100, blank=True, null=True)

    last_activity = models.IntegerField('Остання активність', default=time.time)

    def __str__(self):
        return self.user.username


class Playlist(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=350)
    main_img = models.ImageField(null=True, blank=True, upload_to='playlist')
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    author = models.ForeignKey('auth.User')

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('UserProfile')
    title = models.CharField(max_length=200)
    text = models.TextField()

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    # category = models.ForeignKey(Category)
    playlist = models.ForeignKey(Playlist, blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    post_img = models.ImageField(null=True, blank=True, upload_to='post')

    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    liking = models.ManyToManyField(User, blank=True)
    class Meta:
        ordering = ('-created_date',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# class Comment(models.Model):
#     post = models.ForeignKey(Post)
#     author = models.ForeignKey(UserProfile)
#     content = models.TextField('Коментар')
#     pub_date = models.DateTimeField('Дата коментування', default=timezone.now)
#
#     def __str__(self):
#         return  self.content[0:200]

