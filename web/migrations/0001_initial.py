# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('for_time', models.DateTimeField(default=datetime.datetime.now)),
                ('notes', models.TextField(default=None, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField()),
                ('behavior', models.CharField(max_length=100, choices=[(b'Can Be A Handful', b'Can Be A Handful'), (b'Generally Good', b'Generally Good'), (b'Very Good', b'Very Good'), (b'Angel', b'Angel')])),
                ('notes', models.TextField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone_number', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=20)),
                ('postal_code', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('slug', models.SlugField(default=None, max_length=100)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=20)),
                ('postal_code', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('age', models.IntegerField()),
                ('is_approved', models.BooleanField(default=False)),
                ('slug', models.CharField(default=None, max_length=200)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SitterBeaconResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chosen', models.BooleanField(default=False)),
                ('sitter_rating', models.IntegerField(default=5, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('sitter_rating_comments', models.TextField(max_length=500)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('beacon', models.ForeignKey(to='web.Beacon')),
                ('sitter', models.ForeignKey(to='web.Sitter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(related_name='children', to='web.Parent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beacon',
            name='created_by',
            field=models.ForeignKey(related_name='beacons', to='web.Parent'),
            preserve_default=True,
        ),
    ]
