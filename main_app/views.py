from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Friend, Restaurant, Hotel

# Define the home view


def home(request):
    friends = Friend.objects.all()
    # Include an .html file extension - unlike when rendering EJS templates
    return render(request, 'home.html')

# define the about


def about(request):
    return render(request, 'about.html')

# define the index meaning show all


def friends_index(request):
    friends = Friend.objects.all()
    return render(request, 'friends/index.html', {
        'friends': friends
    })


# need to write a class in order to add a new friend
class FriendCreate(CreateView):
  # tells us from which model
    model = Friend
    fields = '__all__'\



# need to write a class for updating and deleting
class FriendUpdate(UpdateView):
    model = Friend
    # only add in the array what is allowed to be update
    fields = ['name', 'description', 'age']


# need to write a class for deleting friend input
class FriendDelete(DeleteView):
    model = Friend
    success_url = '/friends'


# need to define friend detail
def friends_detail(request, friend_id):
    friend = Friend.objects.get(id=friend_id)
    id_list = friend.restaurants.all().values_list('id')
    restaurants_friend_doesnt_have = Restaurant.objects.exclude(id__in=id_list)
    return render(request, 'friends/detail.html', {
        'friend': friend,
        'restaurants': restaurants_friend_doesnt_have
    })


def assoc_restaurant(request, friend_id, restaurant_id):
    print(friend_id, restaurant_id)
    friend = Friend.objects.get(id=friend_id)
    friend.restaurants.add(restaurant_id)
    return redirect('detail', friend_id=friend_id)


# Restaurant
class RestaurantList(ListView):
    model = Restaurant


class RestaurantDetail(DetailView):
    model = Restaurant


class RestaurantCreate(CreateView):
    model = Restaurant
    fields = '__all__'


class RestaurantUpdate(UpdateView):
    model = Restaurant
    fields = ['name', 'address', 'description']


class RestaurantDelete(DeleteView):
    model = Restaurant
    success_url = '/restaurants/'


class HotelList(ListView):
    model = Hotel


class HotelDetail(DetailView):
    model = Hotel


class HotelUpdate(UpdateView):
    model = Hotel
    fields = ['name', 'address', 'description']


class HotelCreate(CreateView):
    model = Hotel
    fields = '__all__'


class HotelDelete(DeleteView):
    model = Hotel
    success_url = '/hotels/'


def assoc_hotel(request, hotel_id):
    hotel = Hotel.object.get(id=hotel_id)
    hotel.save()
    print(hotel_id)
    return redirect('detail', hotel_id=hotel_id)
