from django.db import models
from user.models import User

class Rooms(models.Model):
    room_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50,default='general')




class Slot(models.Model):
    start_time = models.DateTimeField(auto_now=False,auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False,auto_now_add=False)
    room = models.ForeignKey(Rooms,null=True,related_name='slots',on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    booked_by = models.ForeignKey(User,related_name='users',null=True,on_delete=models.SET_NULL)

