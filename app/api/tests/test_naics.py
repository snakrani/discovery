from test import cases as case
from test import fixtures as data


class NaicsTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            '&541614': ('root_code', 'equal', '541614'),
            '&541330D': ('root_code', 'equal', '541330'),
            '&541840': ('root_code', 'equal', '541840'),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': ('code', 'root_code', 'description', 'keywords__name'),
        'pagination': {
            '@no_args': {},
            '!page': {'page': 15},
            '@count': {'count': 5},
            '@mixed': {'page': 4, 'count': 10}
        },
        'search': {
            '*search1': ('description', 'matches', 'Environmental'),
            '*search2': ('root_code', 'equal', '541910'),
            '*search3': ('keywords__name', 'equal', 'Automobile driving schools'),
            '-search4': ('code', 'matches', '0000000000000')
        },
        'fields': {
            'code': {
                '*exact': '541330',
                '*iexact': '541712c',
                '@in': ("541711", "238290", "561730B"),
                '@contains': '622',
                '@icontains': 'b',
                '@startswith': '54',
                '@istartswith': '2382',
                '@endswith': 'A',
                '@iendswith': 'c',
                '@regex': '[^\d]+$',
                '@iregex': '^(23|56)'
            },
            'root_code': {
                '@exact': '541330',
                '@iexact': '541712',
                '@in': ("541711", "238290", "561730"),
                '@contains': '622',
                '@icontains': '990',
                '@startswith': '61',
                '@istartswith': '5617',
                '@endswith': '10',
                '@iendswith': '20',
                '@regex': '^[\d]+$',
                '@iregex': '^(23|56)'
            },
            'description': {
                '@exact': 'Outdoor Advertising',
                '@iexact': 'hvac maintenance',
                '@in': ("Payroll Services", "Commissioning Services", "Testing Laboratories"),
                '@contains': 'Accounting',
                '@icontains': 'rEPair',
                '@startswith': 'Engineering',
                '@istartswith': 'r',
                '@endswith': 'Services',
                '@iendswith': 'advertIsing',
                '@regex': '[/]+',
                '@iregex': 'water\s+based'
            },
            'keyword': {
                '@exact': 'Cognitive development',
                '@iexact': 'educational Consultants',
                '@in': ("Fine arts schools", "Investment advice", "Language schools"),
                '@contains': 'consulting',
                '@icontains': 'CONSULTING',
                '@startswith': 'Management',
                '@istartswith': 'edu',
                '@endswith': 'services',
                '@iendswith': 'Services',
                '@regex': '(training|consulting)',
                '@iregex': '^(vocational|strategic)'
            }
        }
    }
    
    
    def initialize(self):
        self.router = 'naics'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_int(base_key + ['root_code'])
        resp.is_not_empty(base_key + ['description'])
    

    def test_mixed_request_found_1(self):
        resp = self.validated_multi_list(q = 'Maintenance', ordering = '-code')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Maintenance'))
        resp.validate_ordering('code', 'desc')

    def test_mixed_request_found_2(self):
        resp = self.validated_multi_list(q = 'Pest', ordering = 'code')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Pest'))
        resp.validate_ordering('code', 'asc')
    
    def test_mixed_request_found_3(self):
        resp = self.validated_multi_list(q = 'Services', ordering = '-description')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Services'))
        resp.validate_ordering('description', 'desc')
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(q = 'Space Man', ordering = 'code')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(q = 'Arghhhhh!!', ordering = '-description')
