from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer
from rest_framework.generics import CreateAPIView
# Create your views here.
class CreateRoomView(CreateAPIView):
    serializer_class=RoomSerializer