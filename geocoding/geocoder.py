from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Geocoder(object):
    NYC = (40.7127, -74.0059)

    def __init__(self, geomodel):
        """
        a geocoder object encapsulates operations to be done on a geo_model (one of our models that extend a GeoDjango
        model and has location fields)
        :param geomodel:
        :return:
        """
        self.geolocator = Nominatim()
        self.geomodel = geomodel

    def geolocate(self):
        address_format = "{addr} {city} {state}"
        address = address_format.format(addr=self.geomodel.address, city=self.geomodel.city, state=self.geomodel.state)

        print "about to geolocate address ", address
        try:
            location = self.geolocator.geocode(address)
        except GeocoderTimedOut:
            location = None

        print "found location ", location
        return location
