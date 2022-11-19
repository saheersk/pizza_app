import email
from re import I
import re
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from . import serializers
from .models import Order

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from drf_yasg.utils import swagger_auto_schema


User=get_user_model()



class HelloOrderView(generics.GenericAPIView):

    @swagger_auto_schema(operation_summary="Hello Order")
    def get(self, request):
        return Response(data={"message": "Hello Orders"}, status=status.HTTP_200_OK)


class OrderCreationListView(generics.GenericAPIView):
    serializer_class=serializers.OrderCreationSerializer
    queryset=Order.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List all orders made")
    def get(self, request):

        orders=Order.objects.all()

        serializers=self.serializer_class(instance=orders, many=True)

        return Response(data=serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create order")
    def post(self, request):
        data=request.data

        serializer=self.serializer_class(data=data)

        user=request.user

        if serializer.is_valid():
            serializer.save(customer=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailerializer
    permission_classes=[IsAdminUser]

    @swagger_auto_schema(operation_summary="Retrieve an order by id")
    def get(self, request, order_id):

       order=get_object_or_404(Order, pk=order_id)

       serializer=self.serializer_class(instance=order)

       return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update an order by id")
    def put(self, request, order_id):
        data=request.data

        order=get_object_or_404(Order, pk=order_id)

        serializer=self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete order by id")
    def delete(self, request, order_id):
       order=get_object_or_404(Order, pk=order)   

       order.delete()
       
       return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class=serializers.OrderStatusSerializer
    permission_classes=[IsAdminUser]

    @swagger_auto_schema(operation_summary="Update status of order by id")
    def put(self, request, order_id):
        order=get_object_or_404(Order, pk=order_id)

        data=request.data

        serializer=self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailerializer
    queryset=Order.objects.all()

    @swagger_auto_schema(operation_summary="Users Orders")
    def get(self, request, user_id):
        user=User.objects.get(pk=user_id)

        orders=Order.objects.all().filter(customer=user)

        serializer=self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserOrderDetail(generics.GenericAPIView):
    serializer_class=serializers.OrderDetailerializer

    @swagger_auto_schema(operation_summary="Users Order by id")
    def get(self, request, user_id, order_id):
        user=User.objects.get(pk=user_id)

        order=Order.objects.all().filter(customer=user).get(pk=order_id)

        serializer=self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create(self, validated_data):
    user=User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        phone_number=validated_data['phone_number'],
    )

    user.set_password(validated_data['password'])

    user.save()

    return user





 


