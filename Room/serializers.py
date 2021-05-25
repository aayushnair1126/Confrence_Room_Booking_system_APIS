from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework import exceptions

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = "__all__"
        extra_kwargs = {'booked_by': {'required': False},
                         'is_available':{'default':True},
                          'room':{'required':False}
                        }

    def validate(self, data):
        is_available = data.get('is_available')
        if is_available == False:
            msg = "slot is booked.can not be updated"
            raise exceptions.ValidationError(msg)
        return data


class RoomSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True,required=False)
    class Meta:
        model = Rooms
        fields = ['id','room_name','description','slots']
        extra_kwargs = {'slots': {'required': False},
                        }

    def create(self, validated_data):
        slots_data = validated_data.pop('slots')
        room = Room.objects.create(**validated_data)
        for track_data in slots_data:
            Slot.objects.create(room = room, **track_data)
        return room

class BookSerializer(serializers.Serializer):
    pass




