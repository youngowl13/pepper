from rest_framework import serializers
from restaurant.models import Restaurant, Cuisine


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['name']


class RestaurantSerializer(serializers.ModelSerializer):
    cuisines = CuisineSerializer(many=True)
    city = serializers.ReadOnlyField(source='city.name')

    class Meta:
        model = Restaurant
        fields = ['ext_id', 'name', 'zomato_id', 'address', 'latitude', 'longitude', 'city', 'image_url', 'do_online_delivery', 'cuisines']
