from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import *
from web.models import *
from web.forms import *
import pdb


class SitterViewSet(viewsets.ModelViewSet):
    model = Sitter
    queryset = Sitter.objects.all()
    serializer_class = SitterSerializer

    @detail_route(methods=['get'])
    def nearby_beacons(self, request, pk=None):
        sitter = self.get_object()
        if not sitter.has_location:
            return Response(status=400, data={'errors': "No location set, can't get beacons"})

        future_beacons = Beacon.objects.upcoming()
        return Response(BeaconSerializer(future_beacons, many=True).data)

    @detail_route(methods=['get'])
    def upcoming_jobs(self, request, pk=None):
        sitter = self.get_object()


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
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
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

    @detail_route(methods=['post'])
    def payment(self, request, pk=None):
        """
        allows the parent to add their payment information
        :param request:
        :param pk:
        :return:
        """
        parent = self.queryset.get(id=pk)
        payment_form = PaymentForm(data=request.DATA)
        if payment_form.is_valid():
            stripe_token = payment_form.cleaned_data.get('stripe_token')
            parent.create_customer(stripe_token)

        return Response(self.serializer_class(parent).data)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ParentViewSet, self).dispatch(*args, **kwargs)

class BeaconViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    model = Beacon
    queryset = Beacon.objects.filter(for_time__gte=datetime.datetime.now())
    serializer_class = BeaconSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(BeaconViewSet, self).dispatch(*args, **kwargs)


class SitterBeaconResponseViewSet(viewsets.ModelViewSet):
    model = SitterBeaconResponse
    queryset = SitterBeaconResponse.objects.all()
    serializer_class = SitterBeaconResponseSerializer

    def create(self, request, *args, **kwargs):
        beacon = Beacon.objects.get(id=request.DATA.get('beacon_id'))
        sitter = Sitter.objects.get(id=request.DATA.get('sitter_id'))
        beacon_response, created = SitterBeaconResponse.objects.get_or_create(beacon=beacon, sitter=sitter)

        return Response(SitterBeaconResponseSerializer(beacon_response))