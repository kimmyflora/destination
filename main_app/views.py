from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Friend, Restaurant, Hotel, Photo

# this is for login stuff
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# FOr Authorization
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # CBV
from .forms import ActivityForm

# stuff for photo upload for aws
import uuid # for random numbers (used in generating photo name)
import boto3 # aws sdk that lets us talk to our s3 bucket
import os # this lets us talk to the .env


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

def profile_view(request):
    # Logic for rendering the profile page
    return render(request, 'home.html')


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
    def form_valid(self, form):
		# assign the logged in user self.request.user
      form.instance.user = self.request.user
      # Let the create view finish adding the row 
      # to psql
      return super().form_valid(form)


# need to write a class for updating and deleting


class FriendUpdate(LoginRequiredMixin, UpdateView):
    fields = '__all__'\



# need to write a class for updating and deleting
class FriendUpdate(UpdateView):
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
    activity_form = ActivityForm()
    print(friend.__dict__)
    return render(request, 'friends/detail.html', {
      'friend': friend,
      'activity_form': activity_form,
      'restaurants': restaurants_friend_doesnt_have
    })

def add_activity(request, friend_id):
    form = ActivityForm(request.POST)
    if form.is_valid() :
        new_activity = form.save(commit=False)
        new_activity.friend_id = friend_id
        new_activity.save()
    return redirect('detail', friend_id=friend_id)    

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


def add_photo(request, restaurant_id):
	# photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = 'friends/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            
            Photo.objects.create(url=url, restaurant_id=restaurant_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('restaurants_detail', pk=restaurant_id)

def add_hotel_photo(request, hotel_id):
	# photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = 'friends/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            
            Photo.objects.create(url=url, hotel_id=hotel_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('hotels_detail', pk=hotel_id)


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
