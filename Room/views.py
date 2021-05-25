from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import login ,logout
from rest_framework.authentication import SessionAuthentication,BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions

def is_overlap(data):
    end_slot = Slots.objects.filter(end_time__gt=data.start_time).exclude(id = data.id).order_by('start_time')
    if end_slot.count() != 0:
        flag1 = end_slot.first().start_time > data.start_time
    else:
        flag1 = True
    start_slot = Slots.objects.filter(start_time__lt=data.end_time ).exclude(id = data.id).order_by('start_time')
    if start_slot.count() != 0:
        flag2 = start_slot.last().start_time < data.start_time
    else:
        flag2 = True

    return flag1 and flag2


class CreateRooms(generics.GenericAPIView):
    serializer_class = RoomSerializer
   

    def get(self,request):
        try:
            room = self.request.query_params.get('search_room')
            rooms = Rooms.objects.filter(room_name__icontains = room)
            serializer = RoomSerializer(rooms, many=True)
            return Response({'status':status.HTTP_200_OK,
                             'msg':'rooms retrived',
                             'data':serializer.data})
        except:
            room = Rooms.objects.all()
            serializer = RoomSerializer(room, many=True)
            return Response({'status':status.HTTP_200_OK,
                             'msg':'rooms retrived',
                             'data':serializer.data})

    def post(self,request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_201_CREATED,
                             'msg':'room added',
                             'room detail':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetail(generics.GenericAPIView):
    serializer_class = RoomSerializer

    def get_object(self, id):
        try:
            return Rooms.objects.get(id=id)
        except Rooms.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,
                             'msg':'Room does not exist'},status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        room = self.get_object(id)
        serializer = RoomSerializer(room)
        return Response({'status':status.HTTP_200_OK,
                             'msg':'room retrived',
                             'data':serializer.data})

    def post(self, request, id):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            room = Rooms.objects.get(id=id)
            data.room = room
            data.save()
            flag = is_overlap(data)
            if flag and (data.start_time < data.end_time):
                return Response({'status':status.HTTP_201_CREATED,
                                 'msg':'slot added',
                                 'slot detail':serializer.data}, status=status.HTTP_201_CREATED)
            else:
                data.delete()
                return Response({'status': status.HTTP_400_BAD_REQUEST,
                                 'msg': 'time overlapping or incorrect timings'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        room = self.get_object(id)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,
                             'msg':'room updted',
                             'room detail':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        room = self.get_object(id)
        room.delete()
        return Response({'status':status.HTTP_204_NO_CONTENT,
                         'msg':'room %s deleted successfully'%room.room_name},status=status.HTTP_204_NO_CONTENT)


class SlotDetail(generics.GenericAPIView):
    serializer_class = SlotSerializer

    def get_object(self,id):
        try:
            return Rooms.objects.get(id=id)
        except Rooms.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,
                             'msg':'Room does not exist'},status=status.HTTP_404_NOT_FOUND)

    def get(self, request ,id):
        room = self.get_object(id)
        serializer = RoomSerializer(room)
        return Response({'status':status.HTTP_200_OK,
                             'msg':'slots retrived',
                             'data':serializer.data})

    def post(self, request,id):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            room = Rooms.objects.get(id=id)
            data.room = room
            data.save()
            flag = is_overlap(data)
            if flag and (data.start_time < data.end_time):

                return Response({'status':status.HTTP_201_CREATED,
                                 'msg':'slot added',
                                 'slot detail':serializer.data}, status=status.HTTP_201_CREATED)
            else:
                data.delete()
                return Response({'status':status.HTTP_400_BAD_REQUEST ,'msg': 'time overlapping or incorrect timings'},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#all edit
class SlotEdit(generics.GenericAPIView):
    serializer_class = SlotSerializer

    def get_object(self, id1):
        try:
            return Slots.objects.get(id=id1)
        except Slots.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,
                             'msg':'slot does not exist'},status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id,id1):
        slot = Slots.objects.get(id=id1)
        serializer = SlotSerializer(slot)
        return Response({'status':status.HTTP_200_OK,
                             'msg':'slot retrived',
                             'data':serializer.data})

    def put(self, request,id,id1):
        slot = self.get_object(id1)
        start_time_prev = slot.start_time
        end_time_prev = slot.end_time
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid() :
            data = serializer.save()
            room = Rooms.objects.get(id=id)
            data.room = room
            data.save()
            if is_overlap(data) and (data.start_time < data.end_time):
                return Response({'status':status.HTTP_200_OK,
                                 'msg':'slot updated',
                                 'slot detail':serializer.data})
            else:
                data.start_time = start_time_prev
                data.end_time = end_time_prev
                data.save()
                return Response({'status':status.HTTP_400_BAD_REQUEST ,'msg': 'time overlapping or incorrect timings'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,id, id1):
        slot = self.get_object(id1)
        slot.delete()
        return Response({'status':status.HTTP_204_NO_CONTENT,
                         'msg':'slot %s deleted successfully'%id1},status=status.HTTP_204_NO_CONTENT)



class BookSlot(generics.GenericAPIView):
    serializer_class = BookSerializer       

    def get_object(self, id1):
        try:
            return Slots.objects.get(id=id1)
        except Slots.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,
                             'msg':'Slot does not exist'},status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id,id1):
        slot = self.get_object(id1)
        serializer = SlotSerializer(slot)
        return Response({'status':status.HTTP_200_OK,
                             'msg':'slot retrived',
                             'data':serializer.data})

    def post(self, request,id,id1):
        slot=Slots.objects.get(id=id1)
        if slot.is_available:
            slot.is_available=False
            slot.booked_by = request.user
            slot.save()
            serializer=SlotSerializer(slot)
            return Response({'status':status.HTTP_200_OK,
                             'info':serializer.data,
                             'msg':"booked"})
        else:
            return Response({'status':status.HTTP_226_IM_USED,
                             'msg':"already booked"},status=status.HTTP_226_IM_USED)

    def delete(self,request,id,id1):
        slot = Slots.objects.get(id=id1)
        if slot.is_available==False and slot.booked_by.id == request.user.id :
            slot.is_available = True
            slot.booked_by = None
            slot.save()
            serializer = SlotSerializer(slot)
            return Response({'status':status.HTTP_200_OK,
                             'info': serializer.data,
                             'msg': "unbooked"})
        else:
            return Response({'status':status.HTTP_405_METHOD_NOT_ALLOWED,
                             'You are not allowed':request.user.id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)









