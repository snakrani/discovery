# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0016_fpdsload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpdscontract',
            name='piid',
            field=models.CharField(max_length=128),
        ),
    ]
