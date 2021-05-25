from django.contrib import admin
from django.urls import path,include
from . import views
from .views import *

urlpatterns = [
    path('rooms',CreateRooms.as_view()),
    path('rooms/<int:id>',RoomDetail.as_view()),
    path('rooms/<int:id>/slots', SlotDetail.as_view()),
    path('rooms/<int:id>/slots/<int:id1>', SlotEdit.as_view()),
    path('rooms/<int:id>/slots/<int:id1>/book',BookSlot.as_view()),
]