# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0025_auto_20180205_0342'),
    ]

    operations = [
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_1' WHERE id = '1_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_1' WHERE pool_id = '1_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_1' WHERE pool_id = '1_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_1' WHERE id = '1_UR';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_1' WHERE pool_id = '1_UR';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_1' WHERE pool_id = '1_UR';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_2' WHERE id = '2_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_2' WHERE pool_id = '2_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_2' WHERE pool_id = '2_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_2' WHERE id = '2_UR';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_2' WHERE pool_id = '2_UR';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_2' WHERE pool_id = '2_UR';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_3' WHERE id = '3_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_3' WHERE pool_id = '3_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_3' WHERE pool_id = '3_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_3' WHERE id = '3_UE';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_3' WHERE pool_id = '3_UE';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_3' WHERE pool_id = '3_UE';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_4' WHERE id = '4_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_4' WHERE pool_id = '4_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_4' WHERE pool_id = '4_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_4' WHERE id = '4_UR';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_4' WHERE pool_id = '4_UR';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_4' WHERE pool_id = '4_UR';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_5A' WHERE id = '5A_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_5A' WHERE pool_id = '5A_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_5A' WHERE pool_id = '5A_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_5A' WHERE id = '5A_UR';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_5A' WHERE pool_id = '5A_UR';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_5A' WHERE pool_id = '5A_UR';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_5B' WHERE id = '5B_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_5B' WHERE pool_id = '5B_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_5B' WHERE pool_id = '5B_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_5B' WHERE id = '5B_UR';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_5B' WHERE pool_id = '5B_UR';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_5B' WHERE pool_id = '5B_UR';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_SB_6' WHERE id = '6_SB';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_SB_6' WHERE pool_id = '6_SB';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_SB_6' WHERE pool_id = '6_SB';"),
        
        migrations.RunSQL("UPDATE vendors_pool SET id = 'OASIS_6' WHERE id = '6_UR';"),
        migrations.RunSQL("UPDATE vendors_poolpiid SET pool_id = 'OASIS_6' WHERE pool_id = '6_UR';"),
        migrations.RunSQL("UPDATE vendors_pool_naics SET pool_id = 'OASIS_6' WHERE pool_id = '6_UR';"),
    ]
