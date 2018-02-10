# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0030_auto_20180209_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poolpiid',
            name='zone',
        ),
        migrations.AddField(
            model_name='poolpiid',
            name='zone',
            field=models.ForeignKey(to='vendors.Zone', null=True),
        ),
    ]
