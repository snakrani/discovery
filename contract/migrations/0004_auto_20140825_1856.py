# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0003_auto_20140825_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpdscontract',
            name='completion_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='fpdscontract',
            name='date_signed',
            field=models.DateTimeField(null=True),
        ),
    ]
