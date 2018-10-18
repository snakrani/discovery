from django.test import tag

from test import cases as case
from test import fixtures as data


@tag('pricing')
class PricingTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_contract_fixtures()
    schema = {
        'object': {
            'tags': ('pricing_object',),
            '&1': ('code', 'exact', '1'),
            '&M': ('code', 'exact', 'M'),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': {
            'tags': ('pricing_ordering',),
            'fields': ('code', 'name')
        },
        'pagination': {
            'tags': ('pricing_pagination',),
            '@no_args': {},
            '!page': {'page': 25},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 2}
        },
        'search': {
            'tags': ('pricing_search',),
            '@search2': ('name', 'regex', 'Fixed Price'),
            '-search3': ('name', 'regex', '0000000000000')
        },
        'fields': {
            'code': {
                'tags': ('pricing_field', 'token_text'),
                '@exact': 'Y',
                '@iexact': 'u',
                '@in': ('M', '3', 'K', 'Z')
            },
            'name': {
                'tags': ('pricing_field', 'fuzzy_text'),
                '@exact': 'Firm Fixed Price',
                '@iexact': 'firm fixed price',
                '@in': ("Firm Fixed Price", "Time and Materials"),
                '@contains': 'Price',
                '@icontains': 'price',
                '@startswith': 'Cost',
                '@istartswith': 'cost',
                '@endswith': 'Fee',
                '@iendswith': 'fee',
                '@regex': '^Fixed\s+',
                '@iregex': '^fixed\s+'
            }
        }
    }


    def initialize(self):
        self.router = 'pricing'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['name'])
