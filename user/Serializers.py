from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions

class RegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields =  ('id','username','email','password','is_admin')

		extra_kwargs = {'password': {'write_only':True}}

	def create(self, validate_data):
		user = User.objects.create_user(validate_data['username'],validate_data['email'],validate_data['password'])
		return user



class LoginSerializer(serializers.ModelSerializer):

	username = serializers.CharField(max_length=200)
	password = serializers.CharField(max_length=200)

	class Meta:
		model = User
		fields = ['username','password']

	def validate(self, data):

		username = data.get('username', '')
		password = data.get('password', '')
		
		if username and password:
			user = authenticate(username=username,password=password)
			if user:
				if user.is_active:
					data['user']=user
				else:
					msg ="user is deactivated"
					raise exceptions.ValidationError(msg)
			else:
				msg = "Unable to login with given credentials."
				raise exceptions.ValidationError(msg)
		else:
			msg = "provide username and password both."
			raise exceptions.ValidationError(msg)

		return data



class LogoutSerializer(serializers.Serializer):
    pass