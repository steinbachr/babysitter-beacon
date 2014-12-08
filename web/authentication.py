from django.contrib.auth.models import User, check_password
from django.core.exceptions import ObjectDoesNotExist
from web.models import *



class SitterBeaconBackend(object):
    def authenticate(self, cls=None, email=None, password=None):
        parent = None
        try:
            parent = cls.objects.get(email__iexact=email)
            good_password = check_password(password, parent.password)
            if not good_password:
                parent = None
        except ObjectDoesNotExist:
            pass

        return parent

    def get_user(self, cls, user_id):
        try:
            return cls.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None


class ParentBackend(SitterBeaconBackend):
    def authenticate(self, cls=None, email=None, password=None):
        if cls.user_type() == 'Parent':
            return super(ParentBackend, self).authenticate(Parent, email=email, password=password)

    def get_user(self, parent_id):
        return super(ParentBackend, self).get_user(Parent, parent_id)


class SitterBackend(SitterBeaconBackend):
    def authenticate(self, cls=None, email=None, password=None):
        if cls.user_type() == 'Sitter':
            return super(SitterBackend, self).authenticate(Sitter, email=email, password=password)

    def get_user(self, sitter_id):
        return super(SitterBackend, self).get_user(Sitter, sitter_id)