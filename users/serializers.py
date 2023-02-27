from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    ...

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['ext_id'] = user.ext_id
        token['role'] = user.roles.first().get_id_display()
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'ext_id']
        extra_kwargs = {
            'password': {'write_only': True},
            'ext_id': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
