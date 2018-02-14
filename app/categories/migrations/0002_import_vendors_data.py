# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('vendors', '0026_pool_id_update'),
    ]

    operations = [
        migrations.RunSQL("INSERT INTO categories_naics (id, code, root_code, description) SELECT id, short_code, code, description FROM vendors_naics;"),
        migrations.RunSQL("INSERT INTO categories_setaside (id, code, name, description, far_order) SELECT id, code, abbreviation, short_name, far_order FROM vendors_setaside;"),
        migrations.RunSQL("INSERT INTO categories_pool (id, name, number, vehicle, threshold) SELECT id, name, number, vehicle, threshold FROM vendors_pool;"),
    ]
