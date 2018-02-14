# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0015_auto_20140902_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='FPDSLoad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('load_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
