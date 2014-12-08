from django.db import models
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime


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


#####-----< Models >-----#####
class Parent(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True, default=None)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)

    slug = models.SlugField(max_length=100, default=None)
    created_time = models.DateTimeField(auto_now_add=True)

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

    def __unicode__(self):
        return "Parent {name} ({id})".format(name=self.get_full_name(), id=self.id)


class Sitter(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=200)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)

    age = models.IntegerField(choices=[(i, i) for i in range(16, 60)])
    is_approved = models.BooleanField(default=False)
    slug = models.CharField(max_length=200, default=None)
    created_time = models.DateTimeField(auto_now_add=True)

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
    age = models.IntegerField()
    behavior = models.CharField(max_length=100, choices=BEHAVIOR_CHOICES)
    notes = models.TextField(max_length=1000)


#####-----< Receivers >-----#####
@receiver(pre_save, sender=Parent)
def pre_parent_save(sender, instance=None, **kwargs):
    if not instance.id:
        instance.slug = uniq_slugify(instance, Parent)


@receiver(pre_save, sender=Sitter)
def pre_sitter_save(sender, instance=None, **kwargs):
    if not instance.id:
        instance.slug = uniq_slugify(instance, Sitter)
