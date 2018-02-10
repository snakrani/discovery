# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0029_auto_20180207_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZoneState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=50)),
                ('zone', models.ForeignKey(related_name='state', to='vendors.Zone', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='manageremail',
            name='manager',
            field=models.ForeignKey(related_name='email', to='vendors.Manager', null=True),
        ),
        migrations.AlterField(
            model_name='managerphonenumber',
            name='manager',
            field=models.ForeignKey(related_name='phone', to='vendors.Manager', null=True),
        ),
    ]
