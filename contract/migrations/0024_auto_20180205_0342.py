# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0025_auto_20180205_0342'),
        ('contract', '0023_remove_fpdsload_initialized'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceOfPerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_code', models.CharField(max_length=50, null=True)),
                ('country_name', models.CharField(max_length=128, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('zipcode', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='annual_revenue',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='number_of_employees',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='vendor_location',
            field=models.ForeignKey(to='vendors.Location', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='vendor_phone',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='place_of_performance',
            field=models.ForeignKey(to='contract.PlaceOfPerformance', null=True),
        ),
    ]
