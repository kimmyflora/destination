from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'friend_id': self.id})


class Activity(models.Model):
    name = models.CharField(max_length = 100)
    city = models.CharField(max_length = 200)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    def __str__(self):
      return f"{self.name} in {self.city}"


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotels_detail', kwargs={'pk': self.pk})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        if self.restaurant:
            return f"Photo for restaurant_id: {self.restaurant_id} @{self.url}"
        elif self.hotel:
            return f"Photo for hotel_id: {self.hotel_id} @{self.url}"
        else:
            return "Photo without associated restaurant or hotel"
