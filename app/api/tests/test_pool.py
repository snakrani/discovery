from test import cases as case
from test import fixtures as data


class PoolTest(case.APITestCase, metaclass = case.MetaAPISchema):
  
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            '&HCATS_1': ('name', 'iequal', 'HCATS Unrestricted Pool 1'),
            '&BMO_4': ('name', 'iequal', 'Electrical Maintenance'),
            '&OASIS_SB_4': ('name', 'iequal', 'Scientific Research and Development'),
            '#345': (),
            '#ABCDEFG': ()
        },
        'ordering': 'id',
        'pagination': {
            '@no_args': {},
            '!page': {'page': 5},
            '@count': {'count': 3},
            '@mixed': {'page': 2, 'count': 3}
        },
        'search': {
            '@search1': ('name', 'matches', 'Inspection'),
            '*search2': ('id', 'equal', 'BMO_SB_3'),
            '@search3': ('number', 'matches', '2')
        },
        'fields': {
            'id': {
                '*exact': 'BMO_SB_10',
                '*iexact': 'hcaTs_Sb_2',
                '@in': ("BMO_8", "OASIS_4", "HCATS_SB_1")
            },
            'name': {
                '@exact': 'Elevator Maintenance',
                '@iexact': 'janitoRial',
                '@in': ("Roofing Services", "Plumbing and Pipefitting"),
                '@contains': 'Waste',
                '@icontains': 'energy engineering',
                '@startswith': 'HVAC',
                '@istartswith': 'hvac',
                '@endswith': 'Maintenance',
                '@iendswith': 'dEVelopment',
                '@regex': '\d+$',
                '@iregex': 'air.*development$'
            },
            'number': {
                '@exact': '8',
                '@iexact': '9',
                '@in': ('1', '3', '5B', '16')
            },
            'vehicle': {
                '@exact': 'OASIS_SB',
                '@iexact': 'oasis',
                '@in': ("HCATS", "BMO_SB"),
                '@contains': 'SB',
                '@icontains': 'oasis',
                '@startswith': 'O',
                '@istartswith': 'bm',
                '@endswith': 'SB',
                '@iendswith': '_sb',
                '@regex': '^(OASIS|HCATS)_SB$',
                '@iregex': '^(oaSis|hCaTs)_Sb$'
            },
            'threshold': {
                '@exact': '$15 million',
                '@iexact': '$7.5 MILLION',
                '@in': ("1000 employee", "$18 million", "500 employee"),
                '@contains': 'employee',
                '@icontains': 'EmplOYeE',
                '@startswith': '$38.5',
                '@istartswith': '$38.5',
                '@endswith': 'million',
                '@iendswith': 'MillIon',
                '@regex': '^\d+\s+',
                '@iregex': '(500 EMPLOYEE|MILLION)'
            },
            'naics__code': {
                '@exact': '541330',
                '@iexact': '541712c',
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
            'naics__root_code': {
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
        self.router = 'pools'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['id'])
        resp.is_not_empty(base_key + ['name'])
        resp.is_not_empty(base_key + ['number'])
        resp.is_not_empty(base_key + ['vehicle'])
        resp.is_not_empty(base_key + ['threshold'])
        resp.is_not_empty(base_key + ['naics'])
