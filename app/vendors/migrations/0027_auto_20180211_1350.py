# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_managers(apps, schema_editor):
    Vendor = apps.get_model('vendors', 'Vendor')
    
    for vendor in Vendor.objects.all():
        cm, cm_created = vendor.managers.get_or_create(type='CM', name=vendor.cm_name.strip())
        if vendor.cm_phone:
            cm.phone.get_or_create(number=vendor.cm_phone.strip())
        if vendor.cm_email:
            cm.email.get_or_create(address=vendor.cm_email.strip())
            
        pm, pm_created = vendor.managers.get_or_create(type='PM', name=vendor.pm_name.strip())
        if vendor.pm_phone:
            pm.phone.get_or_create(number=vendor.pm_phone.strip())
        if vendor.pm_email:
            pm.email.get_or_create(address=vendor.pm_email.strip())


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0026_pool_id_update'),
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
                ('manager', models.ForeignKey(related_name='email', to='vendors.Manager', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerPhoneNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=128, null=True)),
                ('manager', models.ForeignKey(related_name='phone', to='vendors.Manager', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='manager',
            name='vendor',
            field=models.ForeignKey(related_name='managers', to='vendors.Vendor', null=True),
        ),
        
        migrations.RunPython(migrate_managers),
        
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
        
    ]
