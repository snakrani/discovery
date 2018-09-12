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
            'fields': ('id', 'name', 'tier__number', 'tier__name', 'poc', 'ordering_guide', 'small_business', 'numeric_pool', 'display_number')
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
            'tier__number': {
                'tags': ('vehicle_field', 'tier_field', 'number'),
                '@exact': 3,
                '@lt': 3,
                '@lte': 2, 
                '@gt': 2, 
                '@gte': 2,
                '@range': (2, 3),
                '@in': (1, 2, 3)
            },
            'tier__name': {
                'tags': ('vehicle_field', 'tier_field', 'fuzzy_text'),
                '@exact': 'Multi-Agency Solutions',
                '@iexact': 'multi-agency solutions',
                '@in': ("Multi-Agency Solutions", "Best-in-Class (BIC)"),
                '@contains': 'Agency',
                '@icontains': 'agency',
                '@startswith': 'Multi',
                '@istartswith': 'multi',
                '@endswith': 'Solutions',
                '@iendswith': 'solutions',
                '@regex': 'Best-in-Class.*$',
                '@iregex': '(multi|class)'
            },
            'poc': {
                'tags': ('vehicle_field', 'fuzzy_text'),
                '@exact': 'oasissb@gsa.gov',
                '@iexact': 'OASIS@GSA.GOV',
                '@in': ("oasissb@gsa.gov", "sbhcats@gsa.gov", "fssi.bmo@gsa.gov"),
                '@contains': 'professionalservices',
                '@icontains': 'ProfessionalServices',
                '@startswith': 'oasis',
                '@istartswith': 'OASIS',
                '@endswith': 'gsa.gov',
                '@iendswith': 'GSA.GOV',
                '@regex': '\.gov$',
                '@iregex': '(OASIS|HCATS)'
            },
            'ordering_guide': {
                'tags': ('vehicle_field', 'fuzzy_text'),
                '@exact': 'https://www.gsa.gov/cdnstatic/CONSOLIDATED_OASIS_U_SB_Ordering_Guide_8-15-2018.pdf',
                '@iexact': 'https://WWW.GSA.GOV/cdnstatic/CONSOLIDATED_OASIS_U_SB_Ordering_Guide_8-15-2018.pdf',
                '@in': ("https://www.gsa.gov/cdnstatic/CONSOLIDATED_OASIS_U_SB_Ordering_Guide_8-15-2018.pdf", "https://www.gsa.gov/cdnstatic/General_Supplies__Services/Ordering%20Guide%20V5_0.pdf"),
                '@contains': 'OASIS',
                '@icontains': 'oasis',
                '@startswith': 'https',
                '@istartswith': 'HTTPS',
                '@endswith': 'pdf',
                '@iendswith': 'PDF',
                '@regex': '(OASIS|HCaTS)',
                '@iregex': '(oasis|hcats)'
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
