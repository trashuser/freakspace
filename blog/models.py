from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django_markdown.widgets import MarkdownWidget

class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='user_avatar')

    def __str__(self):
        return self.user.username


class Playlist(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=350)
    main_img = models.ImageField(null=True, blank=True, upload_to='playlist')
    views = models.IntegerField(default=0)
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
    category = models.ForeignKey(Category)
    playlist = models.ForeignKey(Playlist, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    post_img = models.ImageField(null=True, blank=True, upload_to='post')
    views = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

