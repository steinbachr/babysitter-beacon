# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20141213_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=web.models.child_upload_path, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='child',
            name='name',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parent',
            name='header_image',
            field=models.ImageField(default=None, null=True, upload_to=web.models.parent_upload_path, blank=True),
            preserve_default=True,
        ),
    ]
