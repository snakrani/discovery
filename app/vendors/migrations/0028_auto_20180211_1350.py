# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_import_vendors_data'),
        ('vendors', '0027_auto_20180211_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pool',
            name='naics',
        ),
        migrations.AddField(
            model_name='poolpiid',
            name='zone',
            field=models.ForeignKey(to='categories.Zone', null=True, on_delete=models.DO_NOTHING),
        ),
        migrations.AlterField(
            model_name='poolpiid',
            name='pool',
            field=models.ForeignKey(to='categories.Pool', on_delete=models.DO_NOTHING),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='pools',
            field=models.ManyToManyField(to='categories.Pool', through='vendors.PoolPIID'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='setasides',
            field=models.ManyToManyField(to='categories.SetAside', blank=True),
        ),

        migrations.DeleteModel(
            name='Naics',
        ),
        migrations.DeleteModel(
            name='SetAside',
        ),
        migrations.DeleteModel(
            name='Pool',
        ),
    ]
