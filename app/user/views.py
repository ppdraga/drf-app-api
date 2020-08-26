# from django.shortcuts import render
from rest_framework import generics
from user.serializers import UserSerializer

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
