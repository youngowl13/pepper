from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.models import City
from utils.serializers import CitySerializer

# Create your views here.


class CityList(APIView):
    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
