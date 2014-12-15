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
    children = ChildSerializer(many=True, read_only=True)
    beacons = BeaconSerializer(many=True, read_only=True)
    header_image = serializers.CharField(source='best_header_image', read_only=True)

    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'email', 'slug', 'header_image', 'state', 'city', 'address', 'postal_code',
                  'children', 'beacons', 'can_create_beacon', 'has_payment_info', 'has_location']


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

