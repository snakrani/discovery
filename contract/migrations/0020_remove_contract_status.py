# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0019_create_indexes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='status',
        ),
    ]
