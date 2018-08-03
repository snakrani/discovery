from django.conf import settings
from django.db.models.query import QuerySet
from django.test import Client, TestCase, LiveServerTestCase

from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome import options as chrome
from selenium.webdriver.firefox import options as firefox

from urllib.parse import urlencode, quote
from datetime import datetime

from discovery.utils import memory_in_mb
from test.common import normalize_list
from test.assertions import TestAssertions
from test.validators import VALIDATION_MAP, ResponseValidator, APIResponseValidator, AcceptanceResponseValidator

import os
import math
import psutil
import re
import time
import copy
import json


class TestTracker(object):
    
    start_time = None
    
    
    @classmethod
    def start(cls):
        if cls.start_time is None:
            cls.start_time = datetime.now()
    
    @classmethod
    def render_running_time(cls):
        seconds = (datetime.now() - cls.start_time).total_seconds()
        return "{}:{}".format(math.floor(seconds / 60), "{:.0f}".format(seconds % 60).zfill(2))
    
    @classmethod
    def render_memory(cls):
        process = psutil.Process(os.getpid())
        return "{}MB".format(math.floor(process.memory_info().rss / (1024 * 1024)))
    
        
    @classmethod
    def init_request(cls, name, url, key):
        #print("Testing {} [{} / {}]: {}".format(
        #    name,
        #    cls.render_running_time(),
        #    cls.render_memory(),  
        #    url
        #))
        pass


class BaseTestCase(TestCase, TestAssertions):

    # Initialization
    
    def setUp(self):
        TestTracker.start()
        self.initialize()

        
    def initialize(self):
        # Override in subclass
        pass


class RequestMixin(object):
    
    def encode(self, params):
        return urlencode(params)
    
    def encode_str(self, string):
        return quote(string)
    
    def prepare_params(self, params):
        for param, value in params.items():
            if isinstance(value, (list, tuple)):
                params[param] = ",".join(str(val) for val in value)
        
        return params


class RequestTestCase(BaseTestCase, RequestMixin):
    
    client = None
    
    
    # Initialization
    
    def setUp(self):
        self.client = Client()
        super(RequestTestCase, self).setUp()

            
    # Request
    
    def _get_url(self, path, params = {}):
        return "{}{}?{}".format(settings.API_HOST, path, self.encode(params))
    
        
    def fetch_path(self, path, **params):
        params = self.prepare_params(params)
        url = self._get_url(path, params)
        
        TestTracker.init_request('request', url, self.__class__.__name__)
        return ResponseValidator(self.client.get(path, params), self, url)

    
    # Validation
    
    def validated_path(self, path, **params):
        resp = self.fetch_path(path, **params)
        resp.success()
        return resp
    
    def validated_perm_redirect(self, path, **params):
        resp = self.fetch_path(path, **params)
        resp.perm_redirect()
        return resp
    
    def validated_temp_redirect(self, path, **params):
        resp = self.fetch_path(path, **params)
        resp.temp_redirect()
        return resp       
 

class APITestCase(RequestTestCase):
    
    path = None
    
    base_path = '/api'
    router = None
    
    
    # Initialization
    
    def setUp(self):
        super(APITestCase, self).setUp()
        
        if self.router:
            self.router = self.router.lower()
            self.path = "{}/{}".format(self.base_path, self.router)
    
        
    # Request
    
    def prepare_params(self, params):
        params = super(APITestCase, self).prepare_params(params)
        params['test'] = 'true'
        return params
  
    
    def _get_object_path(self, id):
        return self.path + '/' + str(id)
    
    def _get_object_url(self, id, params = {}):
        return self._get_url(self._get_object_path(id), params)
    
    def _get_list_path(self, router = None):
        path = "{}/{}".format(self.path, router) if router else self.path
        return path if re.match(r'/$', path) else "{}/".format(path)
    
    def _get_list_url(self, params = {}, router = None):
        return self._get_url(self._get_list_path(router), params)
    
    
    def fetch_data(self, **params):
        router = params.pop('_router_', None)
        params = self.prepare_params(params)
        url = self._get_list_url(params, router)
        
        TestTracker.init_request('request', url, self.__class__.__name__)
        return APIResponseValidator(self.client.get(self._get_list_path(router), params), self, url)
    
    def fetch_object(self, id, **params):
        params = self.prepare_params(params)
        url = self._get_object_url(id, params)
        
        TestTracker.init_request('object', url, self.__class__.__name__)
        return APIResponseValidator(self.client.get(self._get_object_path(id), params), self, url)
    
    def fetch_objects(self, **params):
        router = params.pop('_router_', None)
        params = self.prepare_params(params)
        url = self._get_list_url(params, router)
        
        TestTracker.init_request('list', url, self.__class__.__name__)
        return APIResponseValidator(self.client.get(self._get_list_path(router), params), self, url)
    
    
    # Validation
    
    def validated_data(self, **params):
        resp = self.fetch_data(**params)
        resp.success()
        return resp
    
    def validated_list(self, list_count = None, **params):
        validate = params.pop('_validate_', True)
        resp = self.fetch_objects(**params)
        resp.success()
        
        if list_count is not None:
            resp.count(list_count)
        else:
            resp.countMin(1)
        
        if validate:
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

    
    # Utilities
    
    def _check_valid(self, validation_info):
        if not re.search('^[\-\!\#]', validation_info['type']):
            return True
        return False


class MetaAPISchema(type):
    
    def __new__(cls, name, bases, attr):
        if 'schema' in attr and attr['schema']:
            schema = attr['schema']
            
            cls._generate_object_tests(schema.get('object', None), attr)
            cls._generate_ordering_tests(schema.get('ordering', None), attr)
            cls._generate_pagination_tests(schema.get('pagination', None), attr)
            cls._generate_search_tests(schema.get('search', None), attr)
            cls._generate_field_tests(schema.get('fields', None), attr)
            cls._generate_request_tests(schema.get('requests', None), attr)
        
        return super(MetaAPISchema, cls).__new__(cls, name, bases, attr)


    @classmethod
    def _generate_object_tests(cls, object, tests):
        if object is None: return
        
        index = 1
            
        for id, params in object.items():
            info = cls._validation_info(id, '&')
            method_name = "test_object_{}".format(index)
            
            tests[method_name] = cls._object_test_method(info, params)
            index += 1

    @classmethod
    def _generate_ordering_tests(cls, ordering, tests):
        if ordering is None: return
            
        for field in normalize_list(ordering):
            info = {'field': field, 'order': 'asc'}
            tests['test_ordering_{}_asc'.format(field)] = cls._ordering_test_method(info)
            
            info = {'field': field, 'order': 'desc'}
            tests['test_ordering_{}_desc'.format(field)] = cls._ordering_test_method(info)

    @classmethod    
    def _generate_pagination_tests(cls, pagination, tests):
        if pagination is None: return
        
        index_map = {}
        
        for name, params in pagination.items():
            info = cls._validation_info(name, '@')
            lookup = info['lookup']
            
            index_map[lookup] = 1 if lookup not in index_map else index_map[lookup] + 1
            method_name = "test_pagination_{}_{}".format(lookup, index_map[lookup])
            
            tests[method_name] = cls._pagination_test_method(info, params)

    @classmethod    
    def _generate_search_tests(cls, search, tests):
        if search is None: return
        
        index_map = {}
        
        for name, params in search.items():
            info = cls._validation_info(name, '@')
            lookup = info['lookup']
                
            index_map[lookup] = 1 if lookup not in index_map else index_map[lookup] + 1
            method_name = "test_search_{}_{}".format(lookup, index_map[lookup])
            
            tests[method_name] = cls._search_test_method(info, params)
            
    @classmethod        
    def _generate_field_tests(cls, fields, tests):   
        if fields is None: return
        
        index_map = {}
        
        for field, lookups in fields.items():
            field_info = cls._field_info(field)
               
            for lookup, search_value in lookups.items():
                info = cls._validation_info(lookup, '@')
                lookup = info['lookup']
                id = "{}_{}".format(field, lookup)
                
                index_map[id] = 1 if id not in index_map else index_map[id] + 1
                
                if isinstance(search_value, (list, tuple, QuerySet)):
                    search_value = list(search_value)
                
                params = [search_value]
                
                tests["test_field_{}_{}".format(id, index_map[id])] = cls._field_test_method(field_info, info, params)
                tests["test_field_values_{}_{}".format(id, index_map[id])] = cls._field_values_test_method(field_info, info, params)
    
    @classmethod        
    def _generate_request_tests(cls, requests, tests): 
        if requests is None: return
        
        for name, config in requests.items():
            info = cls._validation_info(name, '@')
            method_name = "test_request_{}".format(info['lookup'])
            
            tests[method_name] = cls._request_test_method(info, config)


    @classmethod
    def _object_test_method(cls, info, params):
        def object_test(self):
            resp = getattr(self, info['method'])(info['lookup'])
                    
            if self._check_valid(info) and len(params) == 3:
                field = cls._field_info(params[0])
                validator = VALIDATION_MAP[params[1]]
                search_value = params[2]
                
                if field['relation']:
                    resp.map(validator, [field['base_field']], field['relation'], search_value)
                else:        
                    getattr(resp, validator)(field['name'], search_value)                
        
        return object_test
  
    @classmethod
    def _ordering_test_method(cls, info):
        def ordering_test(self):
            if info['order'] == 'desc':
                info['field'] = "-{}".format(info['field'])
            
            resp = self.validated_multi_list(ordering = info['field'])
            resp.validate_ordering(info['field'], info['order'])
        
        return ordering_test
    
    @classmethod
    def _pagination_test_method(cls, info, params):
        def pagination_test(self):
            page_options = {}
            page = params.get('page', None)
            count = params.get('count', None)
                                
            if page:
                page_options['page'] = page
            if count:
                page_options['count'] = count
                        
            page = 1 if page is None else page   
            resp = getattr(self, info['method'])(**page_options)
                    
            if self._check_valid(info):
                resp.validate_pagination(page, count)
                
        return pagination_test
    
    @classmethod
    def _search_test_method(cls, info, params):
        def search_test(self):
            field = cls._field_info(params[0])
            validator = VALIDATION_MAP[params[1]]
            search_value = params[2]
                
            resp = getattr(self, info['method'])(**{'q': search_value})
                   
            if self._check_valid(info):
                if field['relation']:
                    resp.validate(lambda resp, base_key: resp.map(validator, (base_key + [field['base_field']]), field['relation'], search_value))         
                else:                    
                    resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field['name']], search_value))
        
        return search_test
    
    @classmethod
    def _field_test_method(cls, field, info, params):
        def field_test(self):
            validator = VALIDATION_MAP[info['lookup']]
            field_lookup = field['name'] if info['lookup'] in ('exact', 'date') else "{}__{}".format(field['name'], info['lookup'])
            search_value = params[0]
            
            resp = getattr(self, info['method'])(**{"{}".format(field_lookup): search_value})
            
            if self._check_valid(info):            
                if field['relation']:
                    resp.validate(lambda resp, base_key: resp.map(validator, (base_key + [field['base_field']]), field['relation'], search_value))         
                else:                    
                    resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field['name']], search_value))
        
        return field_test
    
    @classmethod
    def _field_values_test_method(cls, field, info, params):
        def field_values_test(self):
            validator = VALIDATION_MAP[info['lookup']]
            field_lookup = field['name'] if info['lookup'] in ('exact', 'date') else "{}__{}".format(field['name'], info['lookup'])
            search_value = params[0]
            
            resp = getattr(self, info['method'])(**{
                '_router_': "values/{}".format(field['path']),
                '_validate_': False,
                "{}".format(field_lookup): search_value                
            })
            
            if self._check_valid(info):
                resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key, search_value))
        
        return field_values_test

    @classmethod
    def _request_test_method(cls, info, config):
        def request_test(self):
            params = config.get('params', {})
            tests = config.get('tests', [])                  
            resp = getattr(self, info['method'])(**params)
                    
            if self._check_valid(info):
                for test in tests:
                    field = cls._field_info(test[0])
                    validator = test[1]
                    search_value = test[2]
                    
                    if validator == 'ordering':
                        resp.validate_ordering(field['name'], search_value)
                    else:
                        validator = VALIDATION_MAP[validator]
                        
                        if field['relation']:
                            resp.validate(lambda resp, base_key: resp.map(validator, (base_key + [field['base_field']]), field['relation'], search_value))         
                        else:                    
                            resp.validate(lambda resp, base_key: getattr(resp, validator)(base_key + [field['name']], search_value))
                
        return request_test


    @classmethod
    def _validation_info(cls, lookup, default_type = '@'):
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

    @classmethod
    def _field_info(cls, field):
        components = re.split(r'\s*\:\s*', field)
        field_query = components[0]
        field_path = components[1] if len(components) > 1 else field_query
        
        if field_path.find('__') != -1:
            components = field_path.split('__')
            
            base_field = components.pop(0)
            relation = components
        else:
            base_field = field_path
            relation = None
            
        return { 'name': field_query, 'path': field_path, 'base_field': base_field, 'relation': relation }


class AcceptanceTestCase(LiveServerTestCase, TestAssertions, RequestMixin):
    
    drivers = {}
    path = ''
    
    # Initialization
    
    def setUp(self):
        self.base_url = settings.TEST_URL
        self.screenshot_dir = "{}/{}/{}".format(settings.PROJ_DIR, 'logs', 'screenshots')
        
        TestTracker.start()
        
        self.initialize()
        self.init_drivers()
    
    def tearDown(self):
        for name, driver in self.drivers.items():
            driver.quit()

        
    def initialize(self):
        # Override in subclass
        pass
    
    
    def init_drivers(self):
        self.init_chrome()

    def init_chrome(self, tries = 5):
        options = chrome.Options()
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_argument('--disable-gpu')
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        try:
            driver = webdriver.Chrome(chrome_options=options)
            driver.set_page_load_timeout(60)
            
            self.drivers['chrome'] = driver
        
        except WebDriverException as e:
            if tries == 0:
                raise(e)
            else:
                self.init_chrome(tries - 1)   
        
    def init_firefox(self):
        options = firefox.Options()
        options.set_headless()
        
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(60)
        
        self.drivers['firefox'] = driver
    
    
    def _get_url(self, params = {}):
        args = params.pop('args', None)
        
        if args:
            if isinstance(args, (list, tuple)):
                args = list(args)
            else:
                args = [args]
                
            return "{}/{}/{}?{}".format(self.base_url, self.path, "/".join(args), self.encode(params))
        
        return "{}/{}?{}".format(self.base_url, self.path, self.encode(params))
    
    
    def fetch_page(self, test_function, **params):
        params = self.prepare_params(params)
        url = self._get_url(params)
        
        for name, driver in self.drivers.items():
            TestTracker.init_request('request', url, self.__class__.__name__)
            
            driver.get(url)
            
            validator = AcceptanceResponseValidator(driver, self, url)
            validator.wait_for_tag('body')
            
            test_function(validator)


class MetaAcceptanceSchema(type):
    
    def __new__(cls, name, bases, attr):
        if 'schema' in attr and attr['schema']:
            schema = attr['schema']
            
            cls._generate_tests(schema, attr)
        
        return super(MetaAcceptanceSchema, cls).__new__(cls, name, bases, attr)


    @classmethod
    def _generate_tests(cls, object, tests):
        for name, schema in object.items():
            tags = normalize_list(schema.pop('tags', []))
            method_name = "test_{}".format(name)
            single_schema = True
            
            if 'params' in schema:
                params = schema['params']
                
                if isinstance(params, (list, tuple)):
                    for index, param_set in enumerate(list(params)):
                        sub_method_name = "{}_{}".format(method_name, index+1)
                        sub_schema = copy.deepcopy(schema)
                        sub_schema['params'] = param_set
                        tests[sub_method_name] = cls._elem_test_method(name, sub_schema)
                        
                        if len(tags):
                            tests[sub_method_name].tags = tags
                    
                    single_schema = False
            
            if single_schema:
                tests[method_name] = cls._elem_test_method(name, copy.deepcopy(schema))
                
                if len(tags):
                    tests[method_name].tags = tags
            
    
    @classmethod
    def _elem_test_method(cls, name, schema):
        def elem_test(self):
            def tests(resp, data = None):
                if data is None:
                    data = schema
                    
                if isinstance(data, str):
                    getattr(resp, name)(data)
                else:
                    params = data.pop('params', None)
                    wait = data.pop('wait', None)
                    actions = data.pop('actions', {})
                    
                    if wait:
                        if isinstance(wait, (list, tuple)):
                            type = wait[0]
                            elem = wait[1] if len(wait) > 1 else None
                            text = wait[2] if len(wait) > 2 else None
                        else:
                            type = wait
                            elem = None
                            text = None
                        
                        getattr(resp, "wait_for_{}".format(type))(elem, text)
                    
                    for elem, test in data.items():
                        if isinstance(test, (list, tuple)):
                            method = test[0]
                            args = [elem] + list(test[1:])
                        else:
                            method = test
                            args = [elem]                    
                        
                        resp.locator = elem
                        getattr(resp, method)(*args)
                        
                    for action, action_data in actions.items():
                        if action == 'wait':
                            if isinstance(action_data, (list, tuple)):
                                type = action_data[0]
                                elem = action_data[1] if len(action_data) > 2 else None
                                text = action_data[2] if len(action_data) > 2 else None
                            else:
                                type = action_data
                                elem = None
                                text = None
                        
                            getattr(resp, "wait_for_{}".format(type))(elem, text)
                        else:
                            components = action.split('<>')
                            action_elem = components[0]
                            action_event = components[1]
                            action_value = None
                        
                            regex = re.search(r'^([^\[]+)(?:\[([^\]]+)\])?$', action_event, re.IGNORECASE)
                            if regex:
                                action_event = regex.group(1)
                                action_value = regex.group(2)
                            
                                if action_value:
                                    action_value = [value.strip() for value in action_value.split(',')]
                                    action_value = action_value[0] if len(action_value) == 1 else action_value

                            resp.execute(action_elem, action_event, action_value)
                            #resp.screenshot(name, action)

                            tests(resp, action_data)
        
            if 'params' in schema:
                self.fetch_page(tests, **schema['params'])
            else:
                self.fetch_page(tests)
        
        return elem_test
