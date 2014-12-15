from django.db import models
from django.contrib.gis.db import models as geo_models
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
import random
import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY


def uniq_slugify(instance, cls):
    """
    a wrapper around slugify that guarantees uniqueness of slugs in the queryset
    :param instance: the object for which to set the slug
    :param cls: the QuerySet parent to enforce uniqueness within
    :return: the slug string to set on instance
    """
    slug = slugify(' '.join([instance.first_name.lower(), instance.last_name.lower()]))
    existing_with_slug = cls.objects.filter(slug=slug)
    if existing_with_slug:
        slug = "{s}-{count}".format(s=slug, count=len(existing_with_slug))

    return slug


def parent_upload_path(instance, filename):
    return 'parents/{id}/header'.format(id=instance.id)


def child_upload_path(instance, filename):
    return 'parents/{id}/child{count}'.format(id=instance.parent.id, count=instance.parent.children.count())


def get_absolute_url(image_path):
    return "{static}{image}".format(static=settings.STATIC_URL, image=image_path)


#####-----< Models >-----#####
class Parent(AbstractBaseUser, geo_models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True, default=None)

    address = models.CharField(max_length=200, blank=True, null=True, default=None)
    city = models.CharField(max_length=200, blank=True, null=True, default=None)
    state = models.CharField(max_length=20, blank=True, null=True, default=None)
    postal_code = models.CharField(max_length=20, blank=True, null=True, default=None)
    lat_lng = geo_models.PointField(srid=3857, blank=True, null=True, default=None)

    stripe_customer_id = models.CharField(max_length=200, blank=True, null=True, default=None)

    slug = models.SlugField(max_length=100, default=None)
    created_time = models.DateTimeField(auto_now_add=True)
    header_image = models.ImageField(upload_to=parent_upload_path, blank=True, default=None, null=True)

    objects = geo_models.GeoManager()

    is_active = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    #####-----< Abstract Base User Implementation >-----#####
    def get_full_name(self):
        return "{f} {l}".format(f=self.first_name, l=self.last_name)

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def user_type():
        return "Parent"


    #####-----< Properties >-----#####
    @property
    def best_header_image(self):
        header_choices = ["files/images/mountains.jpg", "files/images/space.jpg", "files/images/beach.jpg"]
        return get_absolute_url(self.header_image.path if self.header_image else random.choice(header_choices))

    @property
    def has_payment_info(self):
        return self.stripe_customer_id is not None

    @property
    def has_location(self):
        return (self.state and self.city and self.address and self.postal_code) is not None

    @property
    def can_create_beacon(self):
        return self.has_payment_info and self.has_location

    @property
    def service_cost(self):
        FLAT_FEE = 18
        OUR_FEE = 2

        return (FLAT_FEE + OUR_FEE) * 100


    #####-----< Methods >-----#####
    def create_customer(self, stripe_token):
        if not self.stripe_customer_id:
            customer = stripe.Customer.create(
                card=stripe_token,
                description=self.email
            )

            self.stripe_customer_id = customer.id
            self.save()

    def charge_customer(self):
        stripe.Charge.create(
            amount=self.service_cost,
            currency="usd",
            customer=self.stripe_customer_id
        )

    def __unicode__(self):
        return "Parent {name} ({id})".format(name=self.get_full_name(), id=self.id)


class Sitter(AbstractBaseUser, geo_models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200)

    address = models.CharField(max_length=200, blank=True, null=True, default=None)
    city = models.CharField(max_length=200, blank=True, null=True, default=None)
    state = models.CharField(max_length=20, blank=True, null=True, default=None)
    postal_code = models.CharField(max_length=20, blank=True, null=True, default=None)
    lat_lng = geo_models.PointField(srid=3857, blank=True, null=True, default=None)

    age = models.IntegerField(choices=[(i, i) for i in range(16, 60)], blank=True, null=True, default=None)
    is_approved = models.BooleanField(default=False)
    slug = models.CharField(max_length=200, default=None)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = geo_models.GeoManager()

    is_active = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    #####-----< Abstract Base User Implementation >-----#####
    def get_full_name(self):
        return "{f} {l}".format(f=self.first_name, l=self.last_name)

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def user_type():
        return "Sitter"


    #####-----< Properties >-----#####
    @property
    def jobs(self):
        return SitterBeaconResponse.objects.filter(sitter=self, chosen=True)

    @property
    def completed_jobs(self):
        return self.jobs.filter(beacon__for_time__lte=datetime.datetime.now())

    def __unicode__(self):
        return "Sitter {name} ({id})".format(name=self.get_full_name(), id=self.id)


class Beacon(models.Model):
    created_by = models.ForeignKey(Parent, related_name='beacons')
    created_time = models.DateTimeField(auto_now_add=True)
    for_time = models.DateTimeField(default=datetime.datetime.now)
    notes = models.TextField(blank=True, null=True, default=None)

    @property
    def num_responses(self):
        return SitterBeaconResponse.objects.filter(beacon=self).count()


class SitterBeaconResponse(models.Model):
    sitter = models.ForeignKey(Sitter)
    beacon = models.ForeignKey(Beacon)
    chosen = models.BooleanField(default=False)
    sitter_rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)], default=5)
    sitter_rating_comments = models.TextField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)


class Child(models.Model):
    HANDFUL, GENERALLY_GOOD, VERY_GOOD, ANGEL = "Can Be A Handful", "Generally Good", "Very Good", "Angel"
    BEHAVIOR_CHOICES = (
        (HANDFUL, HANDFUL),
        (GENERALLY_GOOD, GENERALLY_GOOD),
        (VERY_GOOD, VERY_GOOD),
        (ANGEL, ANGEL),
    )

    parent = models.ForeignKey(Parent, related_name='children')
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    behavior = models.CharField(max_length=100, choices=BEHAVIOR_CHOICES)
    notes = models.TextField(max_length=1000)
    image = models.ImageField(upload_to=child_upload_path, blank=True, null=True, default=None)


#####-----< Receivers >-----#####
@receiver(pre_save, sender=Parent)
def pre_parent_save(sender, instance=None, **kwargs):
    if not instance.id:
        instance.slug = uniq_slugify(instance, Parent)


@receiver(pre_save, sender=Sitter)
def pre_sitter_save(sender, instance=None, **kwargs):
    if not instance.id:
        instance.slug = uniq_slugify(instance, Sitter)
