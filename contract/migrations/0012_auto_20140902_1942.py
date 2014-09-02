# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0011_auto_20140902_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fapiisrecord',
            name='vendor',
        ),
        migrations.AddField(
            model_name='fapiisrecord',
            name='duns',
            field=models.CharField(null=True, max_length=15),
            preserve_default=True,
        ),
    ]
