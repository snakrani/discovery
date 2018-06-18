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
        'ordering': ('code', 'description', 'naics__code', 'naics__description'),
        'pagination': {
            '@no_args': {},
            '!page': {'page': 1000},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 3}
        },
        'search': {
            '*search1': ('code', 'matches', 'J041'),
            '*search2': ('description', 'matches', 'Other housekeeping services'),
            '@search3': ('naics__code', 'equal', '561210'),
            '@search4': ('naics__description', 'matches', 'Testing Laboratories'),
            '-search5': ('code', 'matches', '0000000000000')
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
                '@exact': 'Abrasive Materials',
                '@iexact': 'ADP backup and security services',
                '@in': ("Aerial Seeding Services", "Aircraft Components / Accessories"),
                '@contains': 'Snow',
                '@icontains': 'houseKEEPING',
                '@startswith': 'Installation',
                '@istartswith': 'installatION',
                '@endswith': 'System',
                '@iendswith': 'SYSTEM',
                '@regex': '[/]+',
                '@iregex': '^air(craft)?'
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
                '@iexact': 'outdoor advertising',
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
            'naics__sin:naics__sin__code': {
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
            'naics__keyword:naics__keywords__name': {
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
        self.router = 'psc'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        #resp.is_not_empty(base_key + ['description'])
