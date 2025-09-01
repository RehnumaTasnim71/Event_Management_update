from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', default='default.jpg')
    date = models.DateTimeField()
    participants = models.ManyToManyField(User, related_name='rsvp_events', blank=True)

    def __str__(self):
        return self.title
