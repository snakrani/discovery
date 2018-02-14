# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0012_auto_20140902_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fapiisrecord',
            name='piid',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
