from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Friend, Restaurant
from .forms import ActivityForm


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
    fields = ['name', 'description', 'age']
  


    
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
    activity_form = ActivityForm()
    print(friend.__dict__)
    return render(request, 'friends/detail.html', {
      'friend': friend,
      'activity_form': activity_form,
      'restaurants': restaurants_friend_doesnt_have
    })


def add_activity(request, friend_id):
	# process the form request form the client
	form = ActivityForm(request.POST)
	# request.POST is like req.body, its the contents of the form
	# validate the form
	if form.is_valid():
		# create an in memory instance (on django) of our data
		# to be added to psql, commit=False, don't save to db yet
		new_activity = form.save(commit=False)
		# now we want to make sure we add the cat id to the new_feeding
		new_activity.friend_id = friend_id
		new_activity.save() # this is adding a feeding row to the feeding table in psql
	return redirect('detail', friend_id=friend_id) #cat_id is the name of the param in the url path, 
	# cat_id, is the id of the cat from the url request



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
