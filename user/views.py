from django.shortcuts import render
from rest_framework.response import Response
from .Serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics,permissions
from django.contrib.auth import login ,logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class RegisterAPI(generics.GenericAPIView):


	serializer_class = RegisterSerializer

	def post(self,request,*args,**kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception = True)
		user = serializer.save()
		return Response({
			'status': status.HTTP_201_CREATED,
			'msg':"You are Registered Successfully",
			"user" :{'username':user.username,'email':user.email},
			})


class LoginView(generics.GenericAPIView):

	serializer_class = LoginSerializer


	def post(self,request,*args,**kwargs):

		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		login(request, user)

		return Response({
			'status': status.HTTP_201_CREATED,
			'msg':"welcome %s, you have logged in" % user.username,
			})

class LogoutView(generics.GenericAPIView):

	serializer_class = LogoutSerializer

	def post(self,request,*args,**kwargs):
		logout(request)

		return Response({
			'status':status.HTTP_204_NO_CONTENT,
			'msg':'you have logged out'})