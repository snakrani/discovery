# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0028_poolpiid_zone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setaside',
            old_name='short_name',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='naics',
            name='short_code',
        ),
        migrations.RemoveField(
            model_name='setaside',
            name='abbreviation',
        ),
        migrations.AddField(
            model_name='naics',
            name='root_code',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='setaside',
            name='name',
            field=models.CharField(max_length=25, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='naics',
            name='code',
            field=models.CharField(unique=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='setaside',
            name='code',
            field=models.CharField(unique=True, max_length=25),
        ),
    ]
