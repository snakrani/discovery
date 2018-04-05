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
        'ordering': ('code', 'description', 'naics__code', 'naics__root_code', 'naics__description'),
        'pagination': {
            '@no_args': {},
            '!page': {'page': 500},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 3}
        },
        'search': {
            '*search1': ('code', 'matches', 'J041'),
            '*search1': ('description', 'matches', 'Other housekeeping services'),
            '@search2': ('naics__code', 'equal', '561210'),
            '@search2': ('naics__description', 'matches', 'Testing Laboratories'),
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
                '@exact': 'Inspect Services / Valves',
                '@iexact': 'install of alarm signal SYStem',
                '@in': ("Maintenance Of Office Buildings", "Maint - Repair Of Household Furnishings"),
                '@contains': 'Snow',
                '@icontains': 'houseKEEPING',
                '@startswith': 'Installation',
                '@istartswith': 'installatION',
                '@endswith': 'System',
                '@iendswith': 'SYSTEM',
                '@regex': '[/]+',
                '@iregex': '^maint\s\/\srepair\s\/\salteration\s\-\s'
            },
            'naics__code': {
                '@exact': '541330',
                '@iexact': '541712c',
                '@in': ("541711", "238290", "561730B"),
                '@contains': '1210',
                '@icontains': 'b',
                '@startswith': '54',
                '@istartswith': '2382',
                '@endswith': 'A',
                '@iendswith': 'c',
                '@regex': '[^\d]+$',
                '@iregex': '^(23|56)'
            },
            'naics__root_code': {
                '@exact': '541330',
                '@iexact': '541712',
                '@in': ("541711", "238290", "561730"),
                '@contains': '1210',
                '@icontains': '990',
                '@startswith': '61',
                '@istartswith': '5617',
                '@endswith': '10',
                '@iendswith': '20',
                '@regex': '^[\d]+$',
                '@iregex': '^(23|56)'
            },
            'naics__description': {
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
            }
        }
    }
    
    
    def initialize(self):
        self.router = 'psc'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['description'])
