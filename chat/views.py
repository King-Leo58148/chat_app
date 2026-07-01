from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer
from rest_framework.generics import CreateAPIView
from  . consumers import active_users
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CreateRoomView(CreateAPIView):
    serializer_class=RoomSerializer


@api_view(['GET'])
def count_active_users(request,room_name):
    return Response({'count': len(active_users.get(room_name,[]))})
