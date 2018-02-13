# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0024_auto_20180205_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Naics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=25)),
                ('root_code', models.CharField(max_length=25, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'Pool', max_length=128)),
                ('number', models.CharField(max_length=128)),
                ('vehicle', models.CharField(max_length=20, choices=[(b'OASIS_SB', b'OASIS Small Business'), (b'OASIS', b'OASIS Unrestricted'), (b'HCATS_SB', b'HCATS Small Business'), (b'HCATS', b'HCATS Unrestricted')])),
                ('threshold', models.CharField(max_length=128, null=True)),
                ('naics', models.ManyToManyField(to='categories.Naics')),
            ],
        ),
        migrations.CreateModel(
            name='SetAside',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=25)),
                ('name', models.CharField(max_length=25, unique=True, null=True)),
                ('description', models.CharField(max_length=128)),
                ('far_order', models.IntegerField(null=True)),
            ],
        ),
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
                ('zone', models.ForeignKey(related_name='state', to='categories.Zone', null=True)),
            ],
        ),
    ]
