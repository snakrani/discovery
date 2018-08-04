from django.test import tag

from test import cases as case
from test import fixtures as data

import json


@tag('zone')
class ZoneTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            'tags': ('zone_object',),
            '&1': ('states__code', 'exact', 'DE'),
            '&3': ('states__code', 'exact', 'FL'),
            '&4': ('id', 'exact', 4),
            '&6': ('states__code', 'exact', 'KS'),
            '#345': (),
            '#ABCDEFG': ()
        },
        'ordering': {
            'tags': ('zone_ordering',),
            'fields': ('id',)
        },
        'pagination': {
            'tags': ('zone_pagination',),
            '@no_args': {},
            '!page': {'page': 3},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 2}
        },
        'fields': {
            'id': {
                'tags': ('zone_field', 'number'),
                '*exact': 2,
                '@lt': 4,
                '@lte': 4, 
                '@gt': 3, 
                '@gte': 3,
                '@range': (2, 5),
                '@in': (2, 3, 5)
            },
            'states__code': {
                'tags': ('zone_field', 'token_text'),
                '*exact': 'PA',
                '*iexact': 'mE',
                '@in': ('PA', 'NC', 'TX', 'NY')
            }
        },
        'requests': {
            '*r1': {
                'tags': ('zone_request',),
                'params': {'id': 1, 'states__code__iexact': 'md'},
                'tests': (
                    ('id', 'exact', 1),
                    ('states__code', 'exact', 'MD')
                )
            },
            '@r2': {
                'tags': ('zone_request',),
                'params': {'filters': '(states__code__iexact=ct)&(states__code__iexact=nH)'},
                'tests': (
                    ('states__code', 'in', ('CT', 'NH')),
                )
            },
            '-r3': {
                'tags': ('zone_request',),
                'params': {'id': 625, 'states__code': 'NC'}
            },
            '-r4': {
                'tags': ('zone_request',),
                'params': {'filters': '(states__code=GA)&(states__code=IA)'}
            }
        }
    }

    
    def initialize(self):
        self.router = 'zones'
        
    def validate_object(self, resp, base_key = []):
        resp.is_int(base_key + ['id'])
        resp.is_not_empty(base_key + ['states'])
