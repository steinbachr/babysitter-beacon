# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20141213_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='address',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='city',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=3857, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='postal_code',
            field=models.CharField(default=None, max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='parent',
            name='state',
            field=models.CharField(default=None, max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='address',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='age',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='city',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=3857, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='postal_code',
            field=models.CharField(default=None, max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='state',
            field=models.CharField(default=None, max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
