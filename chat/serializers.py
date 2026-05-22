from rest_framework import serializers
from .models import Room, Messages

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']