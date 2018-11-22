from django.test import tag

from test import cases as case
from test import fixtures as data


@tag('placeofperformance')
class PlaceOfPerformanceTest(case.APITestCase, metaclass = case.MetaAPISchema):
    
    fixtures = data.get_contract_fixtures()
    schema = {
        'object': {
            'tags': ('placeofperformance_object',),
            '&10': ('id', 'exact', 10),
            '&25': ('id', 'exact', 25),
            '#77777777': (),
            '#ABCDEFG': ()
        },
        'ordering': {
            'tags': ('placeofperformance_ordering',),
            'fields': ('id', 'country_code', 'country_name', 'state', 'zipcode')
        },
        'pagination': {
            'tags': ('placeofperformance_pagination',),
            '@no_args': {},
            '!page': {'page': 100},
            '@count': {'count': 2},
            '@mixed': {'page': 2, 'count': 2}
        },
        'search': {
            'tags': ('placeofperformance_search',),
            '@search1': ('name', 'regex', 'United States'),
            '@search2': ('name', 'regex', 'NM'),
            '@search3': ('zipcode', 'exact', '80840'),
            '-search4': ('name', 'regex', '0000000000000')
        },
        'fields': {
            'id': {
                'tags': ('placeofperformance_field', 'number'),
                '@exact': 10,
                '@lt': 50,
                '@lte': 50, 
                '@gt': 50, 
                '@gte': 50,
                '@range': (10, 80),
                '@in': (10, 20, 30, 444)
            },
            'country_code': {
                'tags': ('placeofperformance_field', 'location_field', 'token_text'),
                '@exact': 'USA',
                '@iexact': 'usa',
                '@in': ("USA","JPN","MDA","GBR")
            },
            'country_name': {
                'tags': ('placeofperformance_field', 'location_field', 'fuzzy_text'),
                '@exact': 'United States',
                '@iexact': 'united states',
                '@in': ("United States","United Kingdom"),
                '@contains': 'United',
                '@icontains': 'united',
                '@startswith': 'G',
                '@istartswith': 'g',
                '@endswith': 'ia',
                '@iendswith': 'IA',
                '@regex': '^United (States|Kingdom)$',
                '@iregex': '^united (states|kingdom)$'
            },
            'state': {
                'tags': ('placeofperformance_field', 'location_field', 'token_text'),
                '@exact': 'DC',
                '@iexact': 'dc',
                '@in': ("DC","CA","TX","VA")
            },
            'zipcode': {
                'tags': ('placeofperformance_field', 'location_field', 'fuzzy_text'),
                '@exact': '20190',
                '@iexact': '20190',
                '@in': ("20190", "93033", "22102"),
                '@contains': '210',
                '@icontains': '210',
                '@startswith': '35',
                '@istartswith': '35',
                '@endswith': '710',
                '@iendswith': '710',
                '@regex': '^[13579]+',
                '@iregex': '^[13579]+'
            }
        }
    }


    def initialize(self):
        self.router = 'placesofperformance'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['id'])
        resp.is_not_empty(base_key + ['country_code'])
        resp.is_not_empty(base_key + ['country_name'])
