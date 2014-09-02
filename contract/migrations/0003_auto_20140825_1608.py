# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0002_auto_20140825_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpdscontract',
            name='date_signed',
            field=models.DateField(null=True),
        ),
    ]
