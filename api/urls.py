from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter
from api import views as api_views

router = SimpleRouter(trailing_slash=False)
router.register('parents', api_views.ParentViewSet)
router.register('sitters', api_views.SitterViewSet)
router.register('beacons', api_views.BeaconViewSet)
router.register('beacon-responses', api_views.SitterBeaconResponseViewSet)

urlpatterns = router.urls