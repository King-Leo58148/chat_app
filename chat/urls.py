from django.urls import path
from .views import CreateRoomView, count_active_users
urlpatterns = [
    #
    path('create_room/',CreateRoomView.as_view(),name='create-room'),
    path('count_active_users/<str:room_name>/',count_active_users,name='count-active-users')
  
]
