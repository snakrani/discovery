# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0018_auto_20141023_1908'),
    ]

    operations = [
        migrations.RunSQL(""" CREATE INDEX naics_index ON contract_contract ("NAICS"); """),
        migrations.RunSQL(""" CREATE INDEX vendor_index ON contract_contract (vendor_id) """)
    ]
