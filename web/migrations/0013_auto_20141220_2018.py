# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20141220_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitter',
            name='header_image',
            field=models.ImageField(default=None, null=True, upload_to=web.models.sitter_upload_path, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sitter',
            name='profile_image',
            field=models.ImageField(default=None, null=True, upload_to=web.models.sitter_upload_path, blank=True),
            preserve_default=True,
        ),
    ]
