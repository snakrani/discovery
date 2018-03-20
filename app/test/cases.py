from django.conf import settings
from django.db.models.query import QuerySet
from django.test import Client, TestCase

from urllib.parse import urlencode, quote

from test import fixtures as data
from test.common import normalize_list
from test.assertions import DiscoveryAssertions
from test.validators import VALIDATION_MAP, APIResponseValidator

import re


class TestCounter(object):
    counts = {}
    
    @classmethod
    def increment(cls, key):
        if key in cls.counts:
            cls.counts[key] += 1
        else:
            cls.counts[key] = 1
    
    @classmethod
    def get(cls, key):
        if key in cls.counts:
            return cls.counts[key]
        else:
            return 0
        
    @classmethod
    def total(cls):
        total = 0
        
        for key, count in cls.counts.items():
            total += count
            
        return total
    
    @classmethod
    def render(cls, key):
        count = cls.get(key)
        total = cls.total()
        return "[ {} ] - {:.2f}% of {} tests so far".format(count, (count/total)*100, total)


class DiscoveryAPITestCase(TestCase, DiscoveryAssertions):
    
    client = None
    path = None
    router = None
    
    
    # Initialization
    
    def setUp(self):
        self.client = Client()
        self.initialize()
        
        if self.router:
            self.router = self.router.lower()
        
        if not self.path and self.router:
            self.path = "/api/{}/".format(self.router)
    
        
    def initialize(self):
        # Override in subclass
        pass

    
    # Request
    
    def encode(self, params):
        return urlencode(params)
    
    def encode_str(self, string):
        return quote(string)
    
    def prepare_params(self, params):
        for param, value in params.items():
            if isinstance(value, (list, tuple)):
                params[param] = ",".join(str(val) for val in value)
        
        params['test'] = 'true'
        return params
  
    
    def _get_object_path(self, id):
        return self.path + str(id)
    
    def _get_object_url(self, id, params = {}):
        return "{}{}?{}".format(settings.API_HOST, self._get_object_path(id), self.encode(params))
    
    def _get_list_url(self, params = {}):
        return "{}{}?{}".format(settings.API_HOST, self.path, self.encode(params))
    
    
    def fetch_data(self, **params):
        params = self.prepare_params(params)
        url = self._get_list_url(params)
        
        print("Testing request: {}".format(url))
        TestCounter.increment(self.__class__.__name__)
        
        return APIResponseValidator(self.client.get(self.path, params), self, url)
    
    def fetch_object(self, id, **params):
        params = self.prepare_params(params)
        url = self._get_object_url(id, params)
        
        print("Testing object: {}".format(url))
        TestCounter.increment(self.__class__.__name__)
        
        return APIResponseValidator(self.client.get(self._get_object_path(id), params), self, url)
    
    def fetch_objects(self, **params):
        params = self.prepare_params(params)
        url = self._get_list_url(params)
        
        print("Testing list: {}".format(url))
        TestCounter.increment(self.__class__.__name__)
        
        return APIResponseValidator(self.client.get(self.path, params), self, url)

    
    # Validation
    
    def validated_data(self, **params):
        resp = self.fetch_data(**params)
        resp.success()
        return resp
    
    def validated_list(self, list_count = None, **params):
        resp = self.fetch_objects(**params)
        resp.success()
        
        if list_count is not None:
            resp.count(list_count)
        else:
            resp.countMin(1)
        
        resp.validate_list()
        return resp
    
    def validated_single_list(self, **params):
        return self.validated_list(1, **params)
    
    def validated_multi_list(self, **params):
        return self.validated_list(None, **params)
    
    def empty_list(self, **params):
        resp = self.fetch_objects(**params)
        resp.success()
        resp.count(0)
        return resp
    
    def invalid_list(self, **params):
        resp = self.fetch_objects(**params)
        resp.not_found()
        return resp
    
    def validated_object(self, id, **params):
        resp = self.fetch_object(id, **params)
        resp.success()
        resp.validate_object()
        return resp

    def invalid_object(self, id, **params):
        resp = self.fetch_object(id, **params)
        resp.not_found()
        return resp
    
    
    def validate_object(self, resp, base_key = []):
        # Override in subclass
        pass

    
    # Testing
    
    def test_schema(self):
        schema = self.schema()
        object = schema.get('object', None)
        
        def _print_counts():
            print("{}: {}\n".format(
                self.__class__.__name__, 
                TestCounter.render(self.__class__.__name__)
            ))
        
        if object:
            self._test_schema_object(object)
            _print_counts()
        
        elif schema:
            self._test_schema_ordering(schema.get('ordering', None))
            self._test_schema_pagination(schema.get('pagination', None))
            self._test_schema_search(schema.get('search', None))
            self._test_schema_fields(schema.get('fields', None))
            _print_counts()
    
    
    def _test_schema_ordering(self, ordering):
        if ordering:
            for field in normalize_list(ordering):
                with self.subTest(ordering = "{} [asc]".format(field)):
                    resp = self.validated_multi_list(ordering = field)
                    resp.validate_ordering(field, 'asc')
                    
                with self.subTest(ordering = "{} [desc]".format(field)):
                    resp = self.validated_multi_list(ordering = "-{}".format(field))
                    resp.validate_ordering(field, 'desc')                
    
    
    def _test_schema_pagination(self, pagination):
        if pagination:
            for name, params in pagination.items():
                validation = self._validation_info(name, '@')
                
                page = params.get('page', None)
                count = params.get('count', None)
                
                with self.subTest(pagination = "{} [{}]".format(validation['lookup'], validation['type'])):
                    page_options = {}
                    
                    if page:
                        page_options['page'] = page
                    if count:
                        page_options['count'] = count
                        
                    page = 1 if page is None else page   
                    resp = getattr(self, validation['method'])(**page_options)
                    
                    if self._check_valid(validation):
                        resp.validate_pagination(page, count)
    
    
    def _test_schema_search(self, search):
        if search:
            for name, params in search.items():
                validation = self._validation_info(name, '@')
                
                field = params[0]
                validator = params[1]
                search_value = params[2]
                
                with self.subTest(search = "{} [{}]".format(validation['lookup'], validation['type'])):
                    resp = getattr(self, validation['method'])(**{'q': search_value})
                    
                    if self._check_valid(validation):
                        resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field], search_value))
     
        
    def _test_schema_fields(self, fields):   
        if fields:
            for field, lookups in fields.items():
                field_info = self._field_info(field)
                
                for lookup, search_value in lookups.items():
                    validation = self._validation_info(lookup, '@')
                    validator = VALIDATION_MAP[validation['lookup']]
                    
                    field_lookup = field if validation['lookup'] in ('exact', 'date') else "{}__{}".format(field, validation['lookup'])
                        
                    if search_value is None:
                        raise Exception("Search value (string/integer/list) is expected for field lookup")
                        
                    if isinstance(search_value, (list, tuple, QuerySet)):
                        search_value = list(search_value)
                        
                    with self.subTest(field = "{} [{}]".format(field_lookup, validation['type'])):
                        if field_info['relation']:
                            resp = getattr(self, validation['method'])(**{"{}".format(field_lookup): search_value})
                            
                            if self._check_valid(validation):
                                resp.validate(lambda resp, base_key: resp.map(validator, (base_key + [field_info['base_field']]), field_info['relation'], search_value))         
                        else:                    
                            resp = getattr(self, validation['method'])(**{"{}".format(field_lookup): search_value})
                            
                            if self._check_valid(validation):
                                resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field], search_value))

    
    def _test_schema_object(self, object):
        if object:
            for id, params in object.items():
                validation = self._validation_info(id, '&')
                
                with self.subTest(object = "{} [{}]".format(validation['lookup'], validation['type'])):
                    resp = getattr(self, validation['method'])(validation['lookup'])
                    
                    if self._check_valid(validation) and len(params) == 3:
                        field = params[0]
                        validator = params[1]
                        search_value = params[2]
                    
                        getattr(resp, validator)(field, search_value)
                
    
    def schema(self):
        # Override in subclass
        return {}

     
    def _field_info(self, field):
        if field.find('__') != -1:
            components = field.split('__')
            
            base_field = components.pop(0)
            relation = components
        else:
            base_field = field
            relation = None
            
        return { 'base_field': base_field, 'relation': relation }

    
    def _validation_info(self, lookup, default_type = '@'):
        count_specifier = default_type
                    
        if re.search('^[\-\*\@\!\&\#]', lookup):
            count_specifier = lookup[0]
            lookup = lookup[1:]
            
        if count_specifier == '*':
            validation_method = 'validated_single_list'
        elif count_specifier == '-':
            validation_method = 'empty_list'
        elif count_specifier == '!':
            validation_method = 'invalid_list'
        elif count_specifier == '&':
            validation_method = 'validated_object'
        elif count_specifier == '#':
            validation_method = 'invalid_object'
        else:
            validation_method = 'validated_multi_list'
        
        return { 'lookup': lookup, 'method': validation_method, 'type': count_specifier }
    
    
    def _check_valid(self, validation_info):
        if not re.search('^[\-\!\#]', validation_info['type']):
            return True
        return False
    

class CategoryAPITestCase(DiscoveryAPITestCase):
    fixtures = data.get_category_fixtures()


class VendorAPITestCase(DiscoveryAPITestCase):
    fixtures = data.get_vendor_fixtures()


class ContractAPITestCase(DiscoveryAPITestCase):
    fixtures = data.get_contract_fixtures()


class MetadataAPITestCase(DiscoveryAPITestCase):
    fixtures = data.get_metadata_fixtures()
