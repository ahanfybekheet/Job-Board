from .models import *
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = city
        fields = '__all__'