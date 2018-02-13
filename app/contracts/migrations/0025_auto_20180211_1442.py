# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0028_auto_20180211_1350'),
        ('contracts', '0024_auto_20180205_0342'),
    ]

    operations = [
        migrations.RunSQL("UPDATE django_content_type SET app_label = 'contracts' WHERE app_label = 'contract';"),        
        migrations.RunSQL("ALTER TABLE IF EXISTS contract_contract RENAME TO contracts_contract;"),
        migrations.RunSQL("ALTER TABLE IF EXISTS contract_fpdsload RENAME TO contracts_fpdsload;"),
        migrations.RunSQL("ALTER TABLE IF EXISTS contract_placeofperformance RENAME TO contracts_placeofperformance;"),
    ]
