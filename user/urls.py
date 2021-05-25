from django.contrib import admin
from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
