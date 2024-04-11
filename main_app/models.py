from django.db import models
from django.urls import reverse

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurants_detail', kwargs={'pk': self.id})


class Friend(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    restaurants = models.ManyToManyField(Restaurant)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'friend_id': self.id})


class Activity(models.Model):
    name = models.CharField('activity name')
    city = models.CharField('activity location(city)')


    friend = models.ForeignKey(Friend, )
    def __str__(self):
      return f"{self.name} in {self.city}"
