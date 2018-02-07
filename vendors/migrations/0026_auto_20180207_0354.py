# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0025_auto_20180205_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='vehicle',
            field=models.CharField(max_length=20, choices=[(b'OASIS_SB', b'OASIS Small Business'), (b'OASIS', b'OASIS Unrestricted'), (b'HCATS_SB', b'HCATS Small Business'), (b'HCATS', b'HCATS Unrestricted')]),
        ),
    ]
