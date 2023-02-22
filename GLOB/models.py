from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mongoengine import *

class Image(models.Model):
    img = models.ImageField()

class Category(Document):
    name = StringField(max_length=50)

    def __str__(self):
        return self.name


class User(Document):
    username = StringField(max_length=50)
    image = ImageField()
    password = StringField(max_length=50)

    def __str__(self):
        return self.username


class Post(Document):
    title = StringField(max_length=150)
    content = StringField()
    photo = ImageField()
    time_created = DateTimeField(auto_now_add=True)
    time_updated = DateTimeField(auto_now=True)
    cat = ReferenceField(Category)
    user = ReferenceField(User)

    def __str__(self):
        return self.title


class Comments(Document):
    user = ReferenceField(User)
    comment = StringField()
    post = ReferenceField(Post)
    time_created = DateTimeField()
    time_updated = DateTimeField()