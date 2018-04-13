# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0010_fapiisrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='fapiisrecord',
            name='agency_poc_email',
            field=models.EmailField(max_length=75, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fapiisrecord',
            name='agency_poc_name',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fapiisrecord',
            name='agency_poc_phone',
            field=models.CharField(max_length=15, null=True),
            preserve_default=True,
        ),
    ]
