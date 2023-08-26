from rest_framework import serializers
from .models import User, patent


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = patent
        fields = '__all__'
