from test import cases as case
from test import fixtures as data


class PscTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            '&J039': ('code', 'equal', 'J039'),
            '&S208': ('code', 'equal', 'S208'),
            '&H341': ('code', 'equal', 'H341'),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': ('code', 'description', 'naics_code'),
        'pagination': {
            '@no_args': {},
            '!page': {'page': 15},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 3}
        },
        'search': {
            '*search1': ('description', 'matches', 'Other housekeeping services'),
            '@search2': ('naics_code', 'equal', '561210'),
            '-search3': ('code', 'matches', '0000000000000')
        },
        'fields': {
            'code': {
                '*exact': 'N045',
                '*iexact': 's299',
                '@in': ("S202", "Z1DZ", "J034"),
                '@contains': '44',
                '@icontains': '1d',
                '@startswith': 'S2',
                '@istartswith': 's2',
                '@endswith': 'DB',
                '@iendswith': 'db',
                '@regex': '[^\d]+$',
                '@iregex': '^(S2|Z1)'
            },
            'description': {
                '@exact': 'Install of alarm signal system',
                '@iexact': 'install of alarm signal SYStem',
                '@in': ("Maintenance of office buildings", "Maint/repair/alt- office bldgs"),
                '@contains': 'snow',
                '@icontains': 'houseKEEPING',
                '@startswith': 'Installation',
                '@istartswith': 'installatION',
                '@endswith': 'system',
                '@iendswith': 'SYSTEM',
                '@regex': '[/]+',
                '@iregex': '^maint[\s\/]+repair[\s\/]+alt[\s\-]+'
            },
            'naics_code': {
                '@exact': '531312',
                '@iexact': '531312',
                '@in': ("561210", "561621", "561621"),
                '@contains': '173',
                '@icontains': '612',
                '@startswith': '56',
                '@istartswith': '238',
                '@endswith': '210',
                '@iendswith': '21',
                '@regex': '^[\d]+$',
                '@iregex': '^(23|56)'
            }
        }
    }
    
    
    def initialize(self):
        self.router = 'psc'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['description'])
        resp.is_not_empty(base_key + ['naics_code'])
    

    def test_mixed_request_found_1(self):
        resp = self.validated_multi_list(q = 'equipment', ordering = '-code')
        resp.validate(lambda resp, base_key: resp.icontains(base_key + ['description'], 'equipment'))
        resp.validate_ordering('code', 'desc')

    def test_mixed_request_found_2(self):
        resp = self.validated_multi_list(q = 'Maintenance', ordering = 'code')
        resp.validate(lambda resp, base_key: resp.icontains(base_key + ['description'], 'Maintenance'))
        resp.validate_ordering('code', 'asc')
    
    def test_mixed_request_found_3(self):
        resp = self.validated_multi_list(q = 'system', ordering = '-description')
        resp.validate(lambda resp, base_key: resp.icontains(base_key + ['description'], 'system'))
        resp.validate_ordering('description', 'desc')
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(q = 'Space Man', ordering = 'code')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(q = 'Arghhhhh!!', ordering = '-description')
