# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0024_auto_20171217_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('congressional_district', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='annual_revenue',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='number_of_employees',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='sam_address',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='sam_citystate',
        ),
        migrations.AddField(
            model_name='vendor',
            name='sam_location',
            field=models.ForeignKey(to='vendors.Location', null=True, on_delete=models.CASCADE),
        ),
    ]
