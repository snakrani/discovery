from django.test import tag

from test import cases as case
from test import fixtures as data


@tag('status')
class StatusTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_contract_fixtures()
    schema = {
        'object': {
            'tags': ('status_object',),
            '&C1': ('code', 'exact', 'C1'),
            '&L': ('code', 'exact', 'L'),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': {
            'tags': ('status_ordering',),
            'fields': ('code', 'name')
        },
        'pagination': {
            'tags': ('status_pagination',),
            '@no_args': {},
            '!page': {'page': 25},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 2}
        },
        'search': {
            'tags': ('status_search',),
            '@search2': ('name', 'regex', 'Terminated'),
            '-search3': ('name', 'regex', '0000000000000')
        },
        'fields': {
            'code': {
                'tags': ('status_field', 'token_text'),
                '@exact': 'C1',
                '@iexact': 'c1',
                '@in': ('A', 'C2', 'X', 'F')
            },
            'name': {
                'tags': ('status_field', 'fuzzy_text'),
                '@exact': 'Completed',
                '@iexact': 'currEnt',
                '@in': ("Current", "Completed", "Close out"),
                '@contains': 'plete',
                '@icontains': 'PLETE',
                '@startswith': 'C',
                '@istartswith': 'c',
                '@endswith': 'ent',
                '@iendswith': 'ED',
                '@regex': '(Current|Completed)',
                '@iregex': '(current|completed)'
            }
        }
    }


    def initialize(self):
        self.router = 'statuses'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['name'])
