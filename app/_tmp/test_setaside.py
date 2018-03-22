from test import cases as case


class BaseSetasideTest(case.CategoryAPITestCase):
    def initialize(self):
        self.router = 'setasides'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['name'])
        resp.is_not_empty(base_key + ['description'])
        resp.is_int(base_key + ['far_order'])


class SetasideListTest(BaseSetasideTest):
    def schema(self):
        return {
            'ordering': ('code', 'name', 'description', 'far_order'),
            'pagination': {
                '@no_args': {},
                '!page': {'page': 2},
                '@count': {'count': 2},
                '@mixed': {'page': 2, 'count': 2}
            },
            'search': {
                '*search1': ('description', 'matches', 'Veteran'),
                '*search2': ('name', 'equal', 'SDB'),
                '-search3': ('code', 'matches', '0000000000000')
            }
        }
    
    
    def test_mixed_request_found_1(self):
        resp = self.validated_multi_list(q = 'Dis', ordering = '-name')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Dis'))
        resp.validate_ordering('name', 'desc')
    
    def test_mixed_request_found_2(self):
        resp = self.validated_single_list(q = 'QF', ordering = '-code')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['code'], 'QF'))
        resp.validate_ordering('code', 'desc')
    
    def test_mixed_request_found_3(self):
        resp = self.validated_multi_list(q = 'Owned', ordering = 'far_order')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Owned'))
        resp.validate_ordering('far_order', 'asc')
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(q = 'Space Man', ordering = 'code')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(q = 'Arghhhhh!!', ordering = '-description')
    

class SetasideRetrieveTest(BaseSetasideTest):
    def schema(self):
        return {
            'object': {
                '&A5': ('name', 'equal', 'VO'),
                '&XX': ('name', 'equal', 'HubZ'),
                '&A2': ('name', 'equal', 'WO'),
                '#77777777': (),
                '#ABCDEFG': ()
            }
        }
