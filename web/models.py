from django.db import models
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
import datetime


class Parent(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200, blank=True, null=True, default=None)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(decimal_places=4)
    longitude = models.DecimalField(decimal_places=4)

    slug = models.SlugField(max_length=100, default=None)
    created_time = models.DateTimeField(auto_now_add=True)



@receiver(pre_save, sender=Parent)
def pre_sitter_save(sender, instance=None, **kwargs):
    instance.slug = slugify(' '.join([instance.name, instance.id]))


class Sitter(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(decimal_places=4)
    longitude = models.DecimalField(decimal_places=4)

    age = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    slug = models.CharField(default=None)
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def jobs(self):
        return SitterBeaconResponse.objects.filter(sitter=self, chosen=True)

    @property
    def completed_jobs(self):
        return self.jobs.filter(beacon__for_time__lte=datetime.datetime.now())


@receiver(pre_save, sender=Sitter)
def pre_sitter_save(sender, instance=None, **kwargs):
    instance.slug = slugify(' '.join([instance.name, instance.id]))


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
