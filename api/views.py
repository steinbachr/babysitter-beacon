from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import *
from web.models import *
import pdb


class SitterViewSet(viewsets.ModelViewSet):
    model = Sitter
    queryset = Sitter.objects.filter(is_approved=True)


class ChildViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    model = Child
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ChildViewSet, self).dispatch(*args, **kwargs)


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