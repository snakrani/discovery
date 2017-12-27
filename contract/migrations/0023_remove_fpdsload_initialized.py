# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0022_auto_20171211_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fpdsload',
            name='initialized',
        ),
    ]
