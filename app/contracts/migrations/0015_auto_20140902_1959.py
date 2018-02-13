# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0014_auto_20140902_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fapiisrecord',
            name='agency_poc_phone',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
