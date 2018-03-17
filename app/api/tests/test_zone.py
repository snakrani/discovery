from test import cases as case
from api import filters


class BaseZoneTest(case.CategoryAPITestCase):
    def initialize(self):
        self.router = 'zones'
        
    def validate_object(self, resp, base_key = []):
        resp.is_int(base_key + ['id'])
        resp.is_not_empty(base_key + ['states'])


class ZoneListTest(BaseZoneTest):
    def schema(self):
        return {
            'ordering': 'id',
            'pagination': {
                '@no_args': {},
                '!page': {'page': 2},
                '@count': {'count': 2},
                '@mixed': {'page': 2, 'count': 2}
            },
            'fields': {
                'id': {
                    '*exact': '2',
                    '@lt': '4',
                    '@lte': '4', 
                    '@gt': '3', 
                    '@gte': '3',
                    '@range': '2,5',
                    '@in': (2,3,5)
                },
                'state': {
                    '*exact': 'PA',
                    '*iexact': 'mE',
                    '@in': ('PA','NC','TX','NY')
                }
            }
        }
    
       
    def test_mixed_request_found_1(self):
        resp = self.validated_single_list(id = 1, state__iexact = 'md')
        resp.validate(lambda resp, base_key: resp.equal(base_key + ['id'], 1))
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], 'MD'))
    
    def test_mixed_request_found_2(self):
        resp = self.validated_multi_list(filters = self.encode_str('(state__iexact=ct)&(state__iexact=nH)'))
        resp.validate(lambda resp, base_key: resp.includes(base_key + ['states'], ['CT', 'NH']))
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(id = 625, state = 'NC')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(filters = self.encode_str('(state=GA)&(state=IA)'))


class ZoneRetrieveTest(BaseZoneTest):
    def schema(self):
        return {
            'object': {
                '&1': ('states', 'includes', 'DE'),
                '&3': ('states', 'includes', 'FL'),
                '&6': ('states', 'includes', 'KS'),
                '#345': (),
                '#ABCDEFG': ()
            }
        }
