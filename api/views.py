from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import *
from web.models import *


class SitterViewSet(viewsets.ModelViewSet):
    model = Sitter
    queryset = Sitter.objects.filter(is_approved=True)


class ParentViewSet(viewsets.ModelViewSet):
    model = Parent
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    @detail_route(methods=['get'])
    def beacons(self, request, pk=None):
        """
        get the beacons pushed by this parent
        :param request:
        :param pk:
        :return:
        """
        parent = self.queryset.get(id=pk)
        return parent.beacons.all()


class BeaconViewSet(viewsets.ModelViewSet):
    model = Beacon
    queryset = Beacon.objects.filter(for_time__gte=datetime.datetime.now())


class SitterBeaconResponseViewSet(viewsets.ModelViewSet):
    model = SitterBeaconResponse
    queryset = SitterBeaconResponse.objects.all()
    serializer_class = SitterBeaconResponseSerializer

    def create(self, request, *args, **kwargs):
        beacon = Beacon.objects.get(id=request.DATA.get('beacon_id'))
        sitter = Sitter.objects.get(id=request.DATA.get('sitter_id'))
        beacon_response, created = SitterBeaconResponse.objects.get_or_create(beacon=beacon, sitter=sitter)

        return Response(SitterBeaconResponseSerializer(beacon_response))