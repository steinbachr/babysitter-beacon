# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20141220_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=2163, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sitter',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=2163, null=True, blank=True),
            preserve_default=True,
        ),
    ]
