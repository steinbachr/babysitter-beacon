# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20141213_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
