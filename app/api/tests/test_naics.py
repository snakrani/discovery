from test import cases as case


class BaseNaicsTest(case.CategoryAPITestCase):
    def initialize(self):
        self.router = 'naics'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_int(base_key + ['root_code'])
        resp.is_not_empty(base_key + ['description'])


class NaicsListTest(BaseNaicsTest):
    def schema(self):
        return {
            'ordering': ('code', 'root_code', 'description'),
            'pagination': {
                '@no_args': {},
                '!page': {'page': 3},
                '@count': {'count': 5},
                '@mixed': {'page': 4, 'count': 10}
            },
            'search': {
                '*search1': ('description', 'matches', 'Environmental'),
                '*search2': ('root_code', 'equal', '541910'),
                '-search3': ('code', 'matches', '0000000000000')
            }
        }
    
    
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
    

class NaicsRetrieveTest(BaseNaicsTest):
    def schema(self):
        return {
            'object': {
                '&541614': ('root_code', 'iequal', '541614'),
                '&541330D': ('root_code', 'iequal', '541330'),
                '&541840': ('root_code', 'iequal', '541840'),
                '#77777777': (),
                '#ABCDEFG': ()
            }
        }
