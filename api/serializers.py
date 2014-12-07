from rest_framework import serializers
from web.models import *


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['name', 'email', 'slug']


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

