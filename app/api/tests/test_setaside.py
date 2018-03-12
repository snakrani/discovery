from discovery import unit_tests as test


class BaseSetasideTest(test.CategoryAPITestCase):
    def initialize(self):
        self.router = 'setasides'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_not_empty(base_key + ['name'])
        resp.is_not_empty(base_key + ['description'])
        resp.is_int(base_key + ['far_order'])


class SetasideListTest(BaseSetasideTest):
    
    def test_no_args(self):
        self.validated_list(6)
        
    
    def test_search_found_1(self):
        resp = self.validated_list(1, q = 'Veteran')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Veteran'))
    
    def test_search_found_2(self):
        resp = self.validated_list(1, q = 'SDB')
        resp.validate(lambda resp, base_key: resp.equal(base_key + ['name'], 'SDB'))
    
    def test_search_not_found(self):
        self.empty_list(q = '0000000000000')
    
    
    def test_ordering_code(self):
        resp = self.validated_list(6, ordering = 'code')
        resp.validate_ordering('code', 'asc')
    
    def test_ordering_name(self):
        resp = self.validated_list(6, ordering = '-name')
        resp.validate_ordering('name', 'desc')
    
    def test_ordering_description(self):
        resp = self.validated_list(6, ordering = 'description')
        resp.validate_ordering('description', 'asc')
        
    def test_ordering_far_order(self):
        resp = self.validated_list(6, ordering = '-far_order')
        resp.validate_ordering('far_order', 'desc')
    
    
    def test_mixed_request_found_1(self):
        resp = self.validated_list(2, q = 'Dis', ordering = '-name')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Dis'))
        resp.validate_ordering('name', 'desc')
    
    def test_mixed_request_found_2(self):
        resp = self.validated_list(1, q = 'QF', ordering = '-code')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['code'], 'QF'))
        resp.validate_ordering('code', 'desc')
    
    def test_mixed_request_found_3(self):
        resp = self.validated_list(3, q = 'Owned', ordering = 'far_order')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Owned'))
        resp.validate_ordering('far_order', 'asc')
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(q = 'Space Man', ordering = 'code')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(q = 'Arghhhhh!!', ordering = '-description')
    

    def test_pagination_no_args(self):
        resp = self.validated_list(6)
        resp.validate_pagination(1)    
    
    def test_pagination_page_requested(self):
        self.invalid_list(page = 2)
    
    def test_pagination_count_requested(self):
        resp = self.validated_list(6, count = 2)
        resp.validate_pagination(1, 2)
    
    def test_pagination_page_count_requested(self):
        resp = self.validated_list(6, page = 2, count = 2)
        resp.validate_pagination(2, 2)


class SetasideRetrieveTest(BaseSetasideTest):
    
    def test_found_1(self):
        resp = self.validated_object('A5')
        resp.equal('name', 'VO')
    
    def test_found_2(self):
        resp = self.validated_object('XX')
        resp.equal('name', 'HubZ')
    
    def test_found_3(self):
        resp = self.validated_object('A2')
        resp.equal('name', 'WO')
    
    def test_not_found_1(self):
        self.invalid_object('77777777')
    
    def test_not_found_2(self):
        self.invalid_object('ABCDEFG')
