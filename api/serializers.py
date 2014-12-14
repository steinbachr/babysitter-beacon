from rest_framework import serializers
from web.models import *


class BeaconSerializer(serializers.ModelSerializer):
    for_time = serializers.SerializerMethodField()

    def get_for_time(self, obj):
        return obj.for_time

    class Meta:
        model = Beacon
        exclude = []


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ['image']


class ParentSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True)
    beacons = BeaconSerializer(many=True)
    header_image = serializers.CharField(source='best_header_image')

    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'email', 'slug', 'header_image', 'children', 'beacons', 'can_create_beacon']


class SitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitter
        exclude = ['is_approved', 'created_time']


class SitterBeaconResponseSerializer(serializers.ModelSerializer):
    beacon = BeaconSerializer
    sitter = SitterSerializer

    class Meta:
        model = SitterBeaconResponse
        fields = ['beacon', 'sitter']

