from rest_framework import serializers
from restaurant.models import Restaurant, Cuisine
from utils.serializers import CitySerializer
from utils.models import City


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['name', 'ext_id']


class RestaurantSerializer(serializers.ModelSerializer):
    cuisines = CuisineSerializer(many=True)
    city = CitySerializer()

    def create(self, validated_data):
        cuisines = Cuisine.objects.filter(ext_id__in=[d['ext_id'] for d in validated_data.pop('cuisines')])
        city = City.objects.get(ext_id=validated_data.pop('city')['ext_id'])
        instance = Restaurant.objects.create(city=city, **validated_data)
        instance.cuisines.add(*cuisines)
        return instance

    def update(self, instance, validated_data):
        cuisines = Cuisine.objects.filter(ext_id__in=[d['ext_id'] for d in validated_data.pop('cuisines')])
        city = City.objects.get(ext_id=validated_data.pop('city')['ext_id'])
        instance = super().update(instance, validated_data)
        instance.city = city
        instance.cuisines.clear()
        instance.cuisines.add(*cuisines)
        instance.save()
        return instance

    class Meta:
        model = Restaurant
        fields = ['ext_id', 'name', 'zomato_id', 'address', 'latitude', 'longitude', 'city', 'image_url', 'do_online_delivery', 'cuisines']
        read_only_fields = ('ext_id', )


class RestaurantSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['ext_id', 'name']
