# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20141220_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='lat_lng',
        ),
        migrations.RemoveField(
            model_name='sitter',
            name='lat_lng',
        ),
    ]
