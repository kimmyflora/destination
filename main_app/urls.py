from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('friends/', views.friends_index, name='index'),
    path('friends/<int:friend_id>/', views.friends_detail, name='detail'),
    path('friends/create/', views.FriendCreate.as_view(), name='friends_create'),
    # CBV's expect the params to be called pk (convention), which is short for primary key,
    # which is another for id
    path('friends/<int:pk>/update/', views.FriendUpdate.as_view(), name='friends_update'),
    path('friends/<int:pk>/delete/', views.FriendDelete.as_view(), name='friends_delete'),
    path('friends/<int:friend_id>/assoc_restaurant/<int:restaurant_id>/', views.assoc_restaurant, name='assoc_restaurant'),
    path('restaurants/', views.RestaurantList.as_view(), name='restaurants_index'),
    path('restaurants/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurants_detail'),
    path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurants_create'),
    path('restaurants/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurants_update'),
    path('restaurants/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurants_delete'),
    path('add_hotel/', views.add_hotel, name='add_hotel'),
]
