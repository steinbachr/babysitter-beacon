# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20141213_0737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='sitter',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='sitter',
            name='longitude',
        ),
        migrations.AddField(
            model_name='parent',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=3857),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sitter',
            name='lat_lng',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=3857),
            preserve_default=False,
        ),
    ]
