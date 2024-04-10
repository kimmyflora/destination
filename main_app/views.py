from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Friend, Restaurant
# this is for login stuff
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# FOr Authorization
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # CBV


# Define the home view
def signup(request):
    error_message = ''
    if request.method == "POST":
        # create the user form object
        # request.POST is the contents of the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save the user to the database
            user = form.save()  # this adds user to the table in psql
            # login our user
            login(request, user)
            return redirect('index')  # index is the name of the url path
        else:
            error_message = "Invalid signup - try again"
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'error_message': error_message,
        'form': form
    })


def home(request):
    friends = Friend.objects.all()
    # Include an .html file extension - unlike when rendering EJS templates
    return render(request, 'home.html')

# define the about


def about(request):
    return render(request, 'about.html')

# define the index meaning show all

@login_required

def friends_index(request):
    friends = Friend.objects.all()
    return render(request, 'friends/index.html', {
        'friends': friends
    })


# need to write a class in order to add a new friend
class FriendCreate(LoginRequiredMixin, CreateView):
  # tells us from which model
    model = Friend
    fields = ['name', 'description', 'age']


# need to write a class for updating and deleting


class FriendUpdate(LoginRequiredMixin, UpdateView):
    model = Friend
    # only add in the array what is allowed to be update
    fields = ['name', 'description', 'age']

    def form_valid(self, form):
        # assign the logged in user self.request.user
        form.instance.user = self.request.user
        # Let the create view finish adding the row
        # to psql
        return super().form_valid(form)


# need to write a class for deleting friend input

class FriendDelete(LoginRequiredMixin, DeleteView):
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
