from test import cases as case
from test import fixtures as data


class PoolTest(case.APITestCase, metaclass = case.MetaAPISchema):
  
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            '&HCATS_1': ('name', 'iexact', 'HCATS Unrestricted Pool 1'),
            '&BMO_4': ('name', 'iexact', 'Electrical Maintenance'),
            '&OASIS_SB_4': ('name', 'iexact', 'Scientific Research and Development'),
            '#345': (),
            '#ABCDEFG': ()
        },
        'ordering': ('id', 'name', 'number', 'vehicle', 'threshold'),
        'pagination': {
            '@no_args': {},
            '!page': {'page': 15},
            '@count': {'count': 3},
            '@mixed': {'page': 2, 'count': 3}
        },
        'search': {
            '@search1': ('name', 'regex', 'Inspection'),
            '*search2': ('id', 'exact', 'BMO_SB_3'),
            '@search3': ('number', 'regex', '2')
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
                '@iexact': '561710',
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
            'naics__description': {
                '@exact': 'Outdoor Advertising',
                '@iexact': 'meDIA representatives',
                '@in': ("Payroll Services", "Commissioning Services", "Testing Laboratories"),
                '@contains': 'Accounting',
                '@icontains': 'heating',
                '@startswith': 'Engineering',
                '@istartswith': 'r',
                '@endswith': 'Services',
                '@iendswith': 'advertIsing',
                '@regex': 'Services$',
                '@iregex': 'apprentice(ship)?'
            },
            'naics__sin__code': {
                '@exact': '100-03',
                '@iexact': 'c871-202',
                '@in': ("100-03", "520-14", "541-4G", "51-B36-2A"),
                '@contains': '4B',
                '@icontains': '-4b',
                '@startswith': '51',
                '@istartswith': 'c132',
                '@endswith': '03',
                '@iendswith': '2a',
                '@regex': '[A-Z]\d+\-\d+$',
                '@iregex': '^(C87|51)'
            },
            'naics__keywords__name': {
                '@exact': 'Cooking Equipment',
                '@iexact': 'ancillary supplies and / or services',
                '@in': ("Elemental Analyzers", "Energy Consulting Services", "Environmental Consulting Services"),
                '@contains': 'Support',
                '@icontains': 'support',
                '@startswith': 'Marine',
                '@istartswith': 'edu',
                '@endswith': 'Services',
                '@iendswith': 'services',
                '@regex': '(Training|Consulting)',
                '@iregex': '^(vocational|strategic)'
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
        #resp.is_not_empty(base_key + ['threshold'])
        resp.is_not_empty(base_key + ['naics'])
