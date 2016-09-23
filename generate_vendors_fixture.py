#!/usr/local/bin/python
# #!/usr/local/env python

import csv
import json


csv_file_names = [
    'vendor/docs/oasis/pools/Pool 1.csv',
    'vendor/docs/oasis/pools/Pool 2.csv',
    'vendor/docs/oasis/pools/Pool 3.csv',
    'vendor/docs/oasis/pools/Pool 4.csv',
    'vendor/docs/oasis/pools/Pool 5A.csv',
    'vendor/docs/oasis/pools/Pool 5B.csv',
    'vendor/docs/oasis/pools/Pool 6.csv',
    'vendor/docs/oasissb/pools/Pool 1.csv',
    'vendor/docs/oasissb/pools/Pool 2.csv',
    'vendor/docs/oasissb/pools/Pool 3.csv',
    'vendor/docs/oasissb/pools/Pool 4.csv',
    'vendor/docs/oasissb/pools/Pool 5A.csv',
    'vendor/docs/oasissb/pools/Pool 5B.csv',
    'vendor/docs/oasissb/pools/Pool 6.csv',
]

vendors = []

pk_index = 1

for csv_file_name in csv_file_names:
    csv_file = open(csv_file_name, 'r')
    csv_file_reader = csv.reader(csv_file)

    csv_file_reader.next()

    for row in csv_file_reader:
        if row[2] not in [vendor['fields']['duns'] for vendor in vendors]:
            vendor = {
                'fields': {
                    'name': row[0],
                    'duns': row[2],
                    'duns_4': row[2],
                    'cm_name': row[3],
                    'cm_phone': row[4],
                    'cm_email': row[5],
                    'pm_name': row[6],
                    'pm_phone': row[7],
                    'pm_email': row[8]
                },
                'pk': pk_index,
                'model': 'vendor.vendor'
            }

            vendors.append(vendor)

            pk_index += 1

fixture_file_name = 'vendor/fixtures/vendors.json'
fixture_file = open(fixture_file_name, 'w')

json.dump(vendors, fixture_file)
