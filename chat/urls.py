from django.urls import path
from .views import CreateRoomView
urlpatterns = [
    path('create_room/',CreateRoomView.as_view(),name='create-room')
  
]
