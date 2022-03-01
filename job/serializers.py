from .models import *
from rest_framework import serializers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = categorie
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer): 
    class Meta:
        model = job
        fields = '__all__'


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = apply_job
        fields = '__all__'