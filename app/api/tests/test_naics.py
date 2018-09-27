from django.test import tag

from test import cases as case
from test import fixtures as data


@tag('naics')
class NaicsTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            'tags': ('naics_object',),
            '&541614': ('code', 'exact', '541614'),
            '&541330': ('code', 'exact', '541330'),
            '&541840': ('code', 'exact', '541840'),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': {
            'tags': ('naics_ordering',),
            'fields': ('code', 'description')
        },
        'pagination': {
            'tags': ('naics_pagination',),
            '@no_args': {},
            '!page': {'page': 1000},
            '@count': {'count': 5},
            '@mixed': {'page': 4, 'count': 10}
        },
        'search': {
            'tags': ('naics_search',),
            '@search1': ('description', 'regex', 'Water Supply and Irrigation Systems'),
            '*search2': ('code', 'exact', '541910'),
            '-search3': ('code', 'exact', '0000000000000')
        },
        'fields': {
            'code': {
                'tags': ('naics_field', 'fuzzy_text'),
                '*exact': '541330',
                '*iexact': '541713',
                '@in': ("541711", "238290", "561730"),
                '@contains': '622',
                '@icontains': '622',
                '@startswith': '54',
                '@istartswith': '2382',
                '@endswith': '30',
                '@iendswith': '30',
                '@regex': '^54\d+0$',
                '@iregex': '^(23|56)'
            },
            'description': {
                'tags': ('naics_field', 'fuzzy_text'),
                '@exact': 'Outdoor Advertising',
                '@iexact': 'adhesive manufacturing',
                '@in': ("Payroll Services", "Commissioning Services", "Testing Laboratories"),
                '@contains': 'Accounting',
                '@icontains': 'rEPair',
                '@startswith': 'Engineering',
                '@istartswith': 'r',
                '@endswith': 'Services',
                '@iendswith': 'advertIsing',
                '@regex': 'Services$',
                '@iregex': 'similar\s+events'
            },
            'sin__code': {
                'tags': ('naics_field', 'sin_field', 'fuzzy_text'),
                '@exact': '100-03',
                '@iexact': 'c871-202',
                '@in': ("100-03", "520-14", "541-4G", "51-B36-2A"),
                '@contains': 'B36',
                '@icontains': '-b36',
                '@startswith': '51',
                '@istartswith': 'c132',
                '@endswith': '03',
                '@iendswith': '2a',
                '@regex': '[A-Z]\d+\-\d+$',
                '@iregex': '^(C87|51)'
            }
        }
    }
    
    
    def initialize(self):
        self.router = 'naics'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['description'])
