# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20141207_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='email',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitter',
            name='email',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
