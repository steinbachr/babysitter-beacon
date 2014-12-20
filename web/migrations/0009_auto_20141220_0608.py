# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_parent_stripe_customer_id'),
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
