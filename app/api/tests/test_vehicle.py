from django.test import tag

from test import cases as case
from test import fixtures as data


@tag('vehicle')
class VehicleTest(case.APITestCase, metaclass = case.MetaAPISchema):
  
    fixtures = data.get_category_fixtures()
    schema = {
        'object': {
            'tags': ('vehicle_object',),
            '&HCATS': ('name', 'iexact', 'HCATS Unrestricted'),
            '&BMO': ('name', 'iexact', 'BMO Unrestricted'),
            '&OASIS_SB': ('name', 'iexact', 'OASIS Small Business'),
            '#345': (),
            '#ABCDEFG': ()
        },
        'ordering': {
            'tags': ('vehicle_ordering',),
            'fields': ('id', 'name', 'small_business', 'numeric_pool', 'display_number')
        },
        'pagination': {
            'tags': ('vehicle_pagination',),
            '@no_args': {},
            '!page': {'page': 15},
            '@count': {'count': 3},
            '@mixed': {'page': 2, 'count': 3}
        },
        'search': {
            'tags': ('vehicle_search',),
            '@search1': ('name', 'istartswith', 'OASIS'),
            '*search2': ('id', 'exact', 'BMO_SB'),
            '-search3': ('name', 'exact', 'junk')
        },
        'fields': {
            'id': {
                'tags': ('vehicle_field', 'token_text'),
                '*exact': 'BMO_SB',
                '*iexact': 'hcaTs_Sb',
                '@in': ("BMO", "OASIS", "HCATS_SB")
            },
            'name': {
                'tags': ('vehicle_field', 'fuzzy_text'),
                '@exact': 'HCATS Small Business',
                '@iexact': 'hcats small business',
                '@in': ("BMO Small Business", "OASIS Unrestricted"),
                '@contains': 'OASIS',
                '@icontains': 'bmo',
                '@startswith': 'HCATS',
                '@istartswith': 'hcats',
                '@endswith': 'Business',
                '@iendswith': 'unrestricted',
                '@regex': 'Prof.*$',
                '@iregex': 'prof.*$'
            },
            'small_business': {
                'tags': ('vehicle_field', 'boolean'),
                '[1]@exact': True,
                '[2]@exact': False,
            },
            'numeric_pool': {
                'tags': ('vehicle_field', 'boolean'),
                '[1]@exact': True,
                '[2]@exact': False,
            },
            'display_number': {
                'tags': ('vehicle_field', 'boolean'),
                '[1]@exact': True,
                '[2]@exact': False,
            }
        }
    }
        
    
    def initialize(self):
        self.router = 'vehicles'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['id'])
        resp.is_not_empty(base_key + ['name'])
        resp.is_not_empty(base_key + ['small_business'])
        resp.is_not_empty(base_key + ['numeric_pool'])
        resp.is_not_empty(base_key + ['display_number'])
