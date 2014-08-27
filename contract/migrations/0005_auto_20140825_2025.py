# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_auto_20140825_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpdscontract',
            name='agency_id',
            field=models.CharField(max_length=128),
        ),
    ]
