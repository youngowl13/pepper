from restaurant.models import Restaurant, Cuisine
from restaurant.serializers import RestaurantSerializer, RestaurantSelectSerializer, CuisineSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.pagination import PageNumberPagination


class RestaurantList(APIView, PageNumberPagination):
    page_size = 20

    def get(self, request, format=None):
        city = request.GET.get('city')
        name = request.GET.get('search')
        query_set = Restaurant.objects.all().order_by('ext_id')
        if name:
            query_set = query_set.filter(name__icontains=name)
        if city:
            query_set = query_set.filter(city__ext_id=city)
        query_set = self.paginate_queryset(query_set, request, view=self)
        serializer = RestaurantSerializer(query_set, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetail(APIView):

    def get_object(self, ext_id):
        try:
            return Restaurant.objects.get(ext_id=ext_id)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, ext_id, format=None):
        restaurant = self.get_object(ext_id)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, ext_id, format=None):
        restaurant = self.get_object(ext_id)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestaurantSelectList(APIView):
    def get(self, request, format=None):
        restaurant = Restaurant.objects.all()
        serializer = RestaurantSelectSerializer(restaurant, many=True)
        return Response(serializer.data)


class CuisineList(APIView):

    def get(self, request, format=None):
        cuisine = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisine, many=True)
        return Response(serializer.data)
