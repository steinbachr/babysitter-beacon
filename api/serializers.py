from rest_framework import serializers
from web.models import *


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ['image']


class ParentSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True)
    header_image = serializers.CharField(source='best_header_image')

    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'email', 'slug', 'header_image', 'children']


class SitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitter
        exclude = ['is_approved', 'created_time']


class BeaconSerializer(serializers.ModelSerializer):
    created_by = ParentSerializer

    class Meta:
        model = Beacon
        exclude = []


class SitterBeaconResponseSerializer(serializers.ModelSerializer):
    beacon = BeaconSerializer
    sitter = SitterSerializer

    class Meta:
        model = SitterBeaconResponse
        fields = ['beacon', 'sitter']

