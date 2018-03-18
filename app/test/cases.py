from django.conf import settings
from django.db.models.query import QuerySet
from django.test import Client, TestCase

from urllib.parse import urlencode, quote

from test import fixtures as data
from test.common import normalize_list
from test.assertions import ASSERTION_MAP, DiscoveryAssertions
from test.validators import APIResponseValidator

import re


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
    
    def _get_object_path(self, id):
        return self.path + str(id)
    
    def _get_object_url(self, id, params = {}):
        return "{}{}?{}".format(settings.API_HOST, self._get_object_path(id), self.encode(params))
    
    def _get_list_url(self, params = {}):
        return "{}{}?{}".format(settings.API_HOST, self.path, self.encode(params))
    
    
    def fetch_object(self, id, **params):
        url = self._get_object_url(id, params)
        
        print("Testing object: {}".format(url))
        return APIResponseValidator(self.client.get(self._get_object_path(id), params), self, url)
    
    def fetch_objects(self, **params):
        url = self._get_list_url(params)
        
        print("Testing list: {}".format(url))
        return APIResponseValidator(self.client.get(self.path, params), self, url)

    
    # Validation
    
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
        
        if object:
            self._test_schema_object(object)
        
        elif schema:
            with self.subTest(all = "schema"):
                self.validated_multi_list()
            
            self._test_schema_ordering(schema.get('ordering', None))
            self._test_schema_pagination(schema.get('pagination', None))
            self._test_schema_search(schema.get('search', None))
            self._test_schema_fields(schema.get('fields', None))
    
    
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
                
                for lookup, params in lookups.items():
                    params = normalize_list(params)
                    
                    validation = self._validation_info(lookup, '@')
                    validator = ASSERTION_MAP[validation['lookup']]
                    
                    field_lookup = field if validation['lookup'] in ('exact', 'date') else "{}__{}".format(field, validation['lookup'])
                    search_value = params[0]
                        
                    if search_value is None:
                        raise Exception("Search value (string/integer) must be first parameter to lookup")
                        
                    check_value = params[1] if len(params) > 1 else search_value
                    
                    with self.subTest(field = "{} [{}]".format(field_lookup, validation['type'])):
                        if field_info['relation']:
                            resp = getattr(self, validation['method'])(**{"{}".format(field_lookup): search_value})
                            
                            if self._check_valid(validation):
                                resp.validate(lambda resp, base_key: resp.includes((base_key + [field_info['base_field']]), {"{}".format(field_info['relation']): check_value}, validator))         
                        else:                    
                            resp = getattr(self, validation['method'])(**{"{}".format(field_lookup): search_value})
                            
                            if self._check_valid(validation):
                                resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field], check_value))

    
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
            
            base_field = components[0]
            relation = components[1]
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
