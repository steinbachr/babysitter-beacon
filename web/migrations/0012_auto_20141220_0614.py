# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20141220_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sitter',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
