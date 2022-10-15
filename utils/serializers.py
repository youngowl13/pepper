from utils.models import City
from rest_framework.serializers import ModelSerializer


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['ext_id', 'name']
