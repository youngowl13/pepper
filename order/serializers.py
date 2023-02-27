from rest_framework import serializers
from order.models import Order
from restaurant.models import Restaurant


class OrderSerializer(serializers.ModelSerializer):
    restaurant = serializers.SlugRelatedField(slug_field='ext_id', queryset=Restaurant.objects.all())
    restaurant_name = serializers.SerializerMethodField()
    restaurant_address = serializers.SerializerMethodField()

    def create(self, validated_data):
        validated_data['total_price'] = sum(d['price']*d['quantity'] for d in validated_data['product'])
        return Order.objects.create(**validated_data)

    def get_restaurant_name(self, obj):
        return obj.restaurant.name

    def get_restaurant_address(self, obj):
        return obj.restaurant.address

    class Meta:
        model = Order
        fields = ('ext_id', 'restaurant', 'product', 'created', 'total_price', 'restaurant_name', 'restaurant_address')
        read_only_fields = ('ext_id',)
        extra_kwargs = {
            'product': {'write_only': True},
        }
        ordering = ['-created', ]


class OrderDetailSerializer(serializers.ModelSerializer):
    restaurant = serializers.SlugRelatedField(slug_field='ext_id', queryset=Restaurant.objects.all())
    restaurant_name = serializers.CharField(source='restaurant.name')
    restaurant_address = serializers.CharField(source='restaurant.address')

    class Meta:
        model = Order
        fields = ['ext_id', 'restaurant', 'product', 'created', 'total_price', 'restaurant_name', 'restaurant_address']
