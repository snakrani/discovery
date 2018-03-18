from django.db.models.query import QuerySet

from datetime import datetime

from test.common import normalize_list, get_nested_value

import re
import math


ASSERTION_MAP = {
    'isnull': 'is_none',
    'exact': 'equal',
    'iexact': 'iequal',
    'in': 'is_in',
    'contains': 'contains',
    'icontains': 'icontains',
    'startswith': 'startswith',
    'istartswith': 'istartswith',
    'endswith': 'endswith',
    'iendswith': 'iendswith',
    'regex': 'matches',
    'iregex': 'imatches',
    'date': 'startswith',
    'year': 'is_year',
    'month': 'is_month',
    'day': 'is_day',
    'week': 'is_week',
    'week_day': 'is_week_day',
    'quarter': 'is_quarter',
    'range': 'between',
    'lt': 'is_below',
    'lte': 'is_max', 
    'gt': 'is_above', 
    'gte': 'is_min',
}


class DiscoveryAssertions(object):
   
    def assertIsEmpty(self, value, **params):
        if isinstance(value, QuerySet):
            value = list(value)
        
        if not isinstance(value, (str, list, dict)):
            raise AssertionError("Value passed ({}) is not a string, list, or dictionary value".format(str(value)))
        
        if (isinstance(value, (str, list)) and len(value) > 0) or (isinstance(value, dict) and len(value.keys()) > 0):
            raise AssertionError("Value should be empty")
                
    
    def assertIsNotEmpty(self, value, **params):
        if isinstance(value, QuerySet):
            value = list(value)
            
        if not isinstance(value, (str, list, dict)):
            raise AssertionError("Value passed ({}) is not a string, list, or dictionary value".format(str(value)))
        
        if (isinstance(value, (str, list)) and len(value) == 0) or (isinstance(value, dict) and len(value.keys()) == 0):
            raise AssertionError("Value should not be empty")
    
    
    def _check_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False
    
    def _check_float(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False
              
    def assertInteger(self, number, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_int(number):
            raise AssertionError("Value ({}) given is not an integer value".format(number))
             
    def assertFloat(self, number, **params):
        if not number:
            raise AssertionError("Value must be passed as a decimal or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not an decimal value".format(number))

              
    def assertLessThanEqual(self, number, maximum_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) > float(maximum_value):
            raise AssertionError("Value ({}) given is greater than the maximum allowed ({})".format(number, maximum_value))
        
    def assertLessThan(self, number, excluded_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) >= float(excluded_value):
            raise AssertionError("Value ({}) given is not less than ({})".format(number, excluded_value))
              
    def assertGreaterThanEqual(self, number, minimum_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) < float(minimum_value):
            raise AssertionError("Value ({}) given is less than the minimum allowed ({})".format(number, minimum_value))
        
    def assertGreaterThan(self, number, excluded_value, **params):
        if not number:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not a numeric value".format(number))
        
        if float(number) <= float(excluded_value):
            raise AssertionError("Value ({}) given is not greater than ({})".format(number, excluded_value))
   
    def assertBetween(self, number, correct_values, **params):
        if isinstance(correct_values, str): 
            if ',' in correct_values:
                components = correct_values.split(',')
                minimum_value = components[0]
                maximum_value = components[1]
            else:
                AssertionError("Betwen needs multiple values, one ({}) given".format(correct_values))
        else:
            minimum_value = correct_values[0]
            maximum_value = correct_values[1]
        
        self.assertGreaterThanEqual(number, minimum_value)    
        self.assertLessThanEqual(number, maximum_value)


    def assertStrContains(self, value, substring, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as an alpha-numeric string")
        
        if value.find(substring) == -1:
            raise AssertionError("Value ({}) given does not contain {}".format(value, substring))
        
    def assertIStrContains(self, value, substring, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as an alpha-numeric string")
        
        if value.lower().find(substring.lower()) == -1:
            raise AssertionError("Value ({}) given does not contain {}".format(value, substring))
    
    
    def assertMatch(self, value, pattern, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as a alpha-numeric string")
        
        if not re.search(pattern, value):
            raise AssertionError("Value ({}) given does not match pattern {}".format(value, pattern))
        
    def assertIMatch(self, value, pattern, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as a alpha-numeric string")
        
        if not re.search(pattern, value, re.IGNORECASE):
            raise AssertionError("Value ({}) given does not match pattern {}".format(value, pattern))
    
    
    def _convert_date(self, date):
        if not date or not isinstance(date, str) or not re.search('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', date):
            raise AssertionError("Value ({}) must be passed as a date string".format(date))
        
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        
        
    def assertYear(self, date, year, **params):
        date = self._convert_date(date)
        
        if date.year != int(year):
            raise AssertionError("Value ({}) given does not match year {}".format(year, date.year))
        
    def assertMonth(self, date, month, **params):
        date = self._convert_date(date)
        
        if date.month != int(month):
            raise AssertionError("Value ({}) given does not match month {}".format(month, date.month))
        
    def assertDay(self, date, day, **params):
        date = self._convert_date(date)
        
        if date.day != int(day):
            raise AssertionError("Value ({}) given does not match day {}".format(day, date.day))
        
    def assertWeek(self, date, week, **params):
        date = self._convert_date(date)
        date_week = date.isocalendar()[1]
        
        if date_week != int(week):
            raise AssertionError("Value ({}) given does not match week {}".format(week, date_week))
        
    def assertWeekDay(self, date, week_day, **params):
        date = self._convert_date(date)
        date_week_day = max((date.isoweekday() + 1) % 8, 1)
        
        if date_week_day != int(week_day):
            raise AssertionError("Value ({}) given does not match week day {}".format(week_day, date_week_day))
        
    def assertQuarter(self, date, quarter, **params):
        date = self._convert_date(date)
        date_quarter = math.ceil(date.month / 3)
        
        if date_quarter != int(quarter):
            raise AssertionError("Value ({}) given does not match quarter {}".format(quarter, date_quarter))
    
    
    def assertIncludes(self, value, items, **params):
        failed = True
        
        resp = params['resp']
        validator = params['validator']
        
        if isinstance(value, QuerySet):
            value = list(value)
            
        if not value or not isinstance(value, (list, dict)):
            raise AssertionError("Value must be passed as a list or dictionary")
        
        
        def _check_value(data, keys, item):
            try:
                getattr(resp, "{}_data".format(validator))(get_nested_value(data, keys), item)
                return True
            
            except Exception:
                return None        
        
        if isinstance(items, dict):
            keys = next(iter(items))
            items = items[keys]
            
            keys = keys.split('|') if '|' in keys else [keys]
            items = normalize_list(items)
            
            for item in items:
                if isinstance(value, list):
                    for element in value:
                        if _check_value(element, keys, item):
                            failed = False
                else:
                    if _check_value(value, keys, item):
                        failed = False
                
        else:
            if isinstance(items, (str, int, float)):
                items = [items]
        
            for item in items:
                if (isinstance(value, list) and item in value) or (isinstance(value, dict) and value.get(item, None)):
                    failed = False
        
        if failed:    
            raise AssertionError("Value passed ({}) does not include item ({})".format(str(value), item))

