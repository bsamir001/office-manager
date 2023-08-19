from rest_framework import serializers
from .models import User,patent


class userrigister_selizer(serializers.Serializer):
    phone=serializers.CharField(max_length=11)


class Verifycodeselizer(serializers.Serializer):
    code=serializers.IntegerField()

class User_Registerselizer (serializers.ModelSerializer):
    class Meta:
        model = patent
        fields = ('codeID','firstname','lastname','age','typeSickness','typebime','infopatent','textSickness',)