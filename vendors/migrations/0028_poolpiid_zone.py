# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0027_auto_20180207_0636'),
    ]

    operations = [
        migrations.AddField(
            model_name='poolpiid',
            name='zone',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
