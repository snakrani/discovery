# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0017_auto_20140930_1453'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FAPIISRecord',
        ),
        migrations.RemoveField(
            model_name='fpdscontract',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='FPDSContract',
        ),
        migrations.AddField(
            model_name='contract',
            name='reason_for_modification',
            field=models.CharField(max_length=2, choices=[('A', 'Additional Work'), ('B', 'Supplemental Agreement for work within scope'), ('C', 'Funding Only Action'), ('D', 'Change Order'), ('E', 'Terminated for Default'), ('F', 'Terminated for Convenience'), ('G', 'Exercise an Option'), ('H', 'Definitize Letter Contract'), ('J', 'Novation Agreement'), ('K', 'Close out'), ('L', 'Definitize Letter Contract'), ('M', 'Other Adminitrative Action'), ('N', 'Legal Contract Cancellation'), ('P', 'Representation of non-Novated Merger/Acquisitoin'), ('R', 'Rerepresentation'), ('S', 'Change PIID'), ('T', 'Transfer Action'), ('V', 'Vendor DUNS Change'), ('W', 'Vendor Address Change'), ('X', 'Terminated for Cause'), ('C1', 'Completed'), ('C2', 'Current')], null=True),
            preserve_default=True,
        ),
    ]
