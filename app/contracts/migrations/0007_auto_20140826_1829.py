# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0006_auto_20140825_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fpdscontract',
            name='NAICS',
        ),
        migrations.AddField(
            model_name='fpdscontract',
            name='NAICS',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
