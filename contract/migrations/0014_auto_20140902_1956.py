# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0013_auto_20140902_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fapiisrecord',
            name='duns',
            field=models.CharField(max_length=15, db_index=True),
        ),
    ]
