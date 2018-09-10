
from django.conf import settings
from django.db import migrations, models
from django.core.management import call_command


def populate_vehicles(apps, schema_editor):
    call_command('loaddata', "{}/{}".format(settings.BASE_DIR, 'categories/fixtures/vehicles.json'))


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0016_auto_20180801_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('small_business', models.NullBooleanField()),
                ('numeric_pool', models.NullBooleanField()),
                ('display_number', models.NullBooleanField()),
            ],
        ),
        migrations.RunPython(populate_vehicles),
    ]
