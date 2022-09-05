from rest_framework import serializers
from restaurant.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['ext_id', 'name', 'zomato_id', 'address', 'latitude', 'longitude', 'image_url', 'do_online_delivery']
