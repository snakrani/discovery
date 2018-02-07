# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0026_auto_20180207_0354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True)),
                ('type', models.CharField(max_length=10, choices=[(b'CM', b'Contract Manager'), (b'PM', b'Project Manager')])),
            ],
        ),
        migrations.CreateModel(
            name='ManagerEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=128, null=True)),
                ('manager', models.ForeignKey(related_name='emails', to='vendors.Manager', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerPhoneNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=128, null=True)),
                ('manager', models.ForeignKey(related_name='phones', to='vendors.Manager', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='cm_email',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='cm_name',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='cm_phone',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='pm_email',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='pm_name',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='pm_phone',
        ),
        migrations.AddField(
            model_name='manager',
            name='vendor',
            field=models.ForeignKey(related_name='managers', to='vendors.Vendor', null=True),
        ),
    ]
