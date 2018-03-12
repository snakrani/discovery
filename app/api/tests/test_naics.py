from discovery import unit_tests as test


class BaseNaicsTest(test.CategoryAPITestCase):
    def initialize(self):
        self.router = 'naics'
        
    def validate_object(self, resp, base_key = []):
        resp.is_not_empty(base_key + ['code'])
        resp.is_int(base_key + ['root_code'])
        resp.is_not_empty(base_key + ['description'])


class NaicsListTest(BaseNaicsTest):
    
    def test_no_args(self):
        self.validated_list(55)
        
    
    def test_search_found_1(self):
        resp = self.validated_list(1, q = 'Environmental')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Environmental'))
    
    def test_search_found_2(self):
        resp = self.validated_list(1, q = '541910')
        resp.validate(lambda resp, base_key: resp.equal(base_key + ['root_code'], '541910'))
    
    def test_search_not_found(self):
        self.empty_list(q = '0000000000000')
    
    
    def test_ordering_code(self):
        resp = self.validated_list(55, ordering = 'code')
        resp.validate_ordering('code', 'asc')
    
    def test_ordering_root_code(self):
        resp = self.validated_list(55, ordering = '-root_code')
        resp.validate_ordering('root_code', 'desc')
    
    def test_ordering_description(self):
        resp = self.validated_list(55, ordering = 'description')
        resp.validate_ordering('description', 'asc')
    
    
    def test_mixed_request_found_1(self):
        resp = self.validated_list(9, q = 'Maintenance', ordering = '-code')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Maintenance'))
        resp.validate_ordering('code', 'desc')
    
    def test_mixed_request_found_2(self):
        resp = self.validated_list(1, q = 'Pest', ordering = 'code')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Pest'))
        resp.validate_ordering('code', 'asc')
    
    def test_mixed_request_found_3(self):
        resp = self.validated_list(26, q = 'Services', ordering = '-description')
        resp.validate(lambda resp, base_key: resp.matches(base_key + ['description'], 'Services'))
        resp.validate_ordering('description', 'desc')
    
    def test_mixed_request_not_found_1(self):
        self.empty_list(q = 'Space Man', ordering = 'code')
    
    def test_mixed_request_not_found_2(self):
        self.empty_list(q = 'Arghhhhh!!', ordering = '-description')
    

    def test_pagination_no_args(self):
        resp = self.validated_list(55)
        resp.validate_pagination(1)    
    
    def test_pagination_page_requested(self):
        self.invalid_list(page = 3)
    
    def test_pagination_count_requested(self):
        resp = self.validated_list(55, count = 5)
        resp.validate_pagination(1, 5)
    
    def test_pagination_page_count_requested(self):
        resp = self.validated_list(55, page = 4, count = 10)
        resp.validate_pagination(4, 10)


class NaicsRetrieveTest(BaseNaicsTest):
    
    def test_found_1(self):
        resp = self.validated_object('541614')
        resp.equal('root_code', '541614')
    
    def test_found_2(self):
        resp = self.validated_object('541330D')
        resp.equal('root_code', '541330')
    
    def test_found_3(self):
        resp = self.validated_object('541840')
        resp.equal('root_code', '541840')
    
    def test_not_found_1(self):
        self.invalid_object('77777777')
    
    def test_not_found_2(self):
        self.invalid_object('ABCDEFG')
