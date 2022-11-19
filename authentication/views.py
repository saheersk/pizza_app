from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from . import serializers


class HelloAuthView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello view")
    def get(self, request):
        return Response(data={"message": "HelloAuthView"}, status=status.HTTP_200_OK)


class UserCreateView(generics.GenericAPIView):

    serializer_class=serializers.UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self, request):
        data=request.data

        serializers=self.serializer_class(data=data)

        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_200_OK)

        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
