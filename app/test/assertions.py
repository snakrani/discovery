from datetime import datetime
from django.db.models.query import QuerySet

from test.common import normalize_list, get_nested_value

import re
import math


class TestAssertions(object):
   
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
            
        if not isinstance(value, (bool, int, float, str, list, dict)):
            raise AssertionError("Value passed ({}) is not a boolean, int, float, string, list, or dictionary value".format(str(value)))
        
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
        if number is None:
            raise AssertionError("Value must be passed as a integer or numeric string")
        
        if not self._check_int(number):
            raise AssertionError("Value ({}) given is not an integer value".format(number))
             
    def assertFloat(self, number, **params):
        if number is None:
            raise AssertionError("Value must be passed as a decimal or numeric string")
        
        if not self._check_float(number):
            raise AssertionError("Value ({}) given is not an decimal value".format(number))

              
    def assertLessThanEqual(self, text, maximum_value, **params):
        if text is None:
            raise AssertionError("Value must be passed as a number or string")
        
        if isinstance(text, str):
            if text > maximum_value:
                raise AssertionError("Value ({}) given is greater than the maximum allowed ({})".format(text, maximum_value))
        else:
            if not self._check_float(text):
                raise AssertionError("Value ({}) given is not a numeric or string value".format(text))
        
            if float(text) > float(maximum_value):
                raise AssertionError("Value ({}) given is greater than the maximum allowed ({})".format(text, maximum_value))
        
    def assertLessThan(self, text, excluded_value, **params):
        if text is None:
            raise AssertionError("Value must be passed as a number or string")
        
        if isinstance(text, str):
            if text >= excluded_value:
                raise AssertionError("Value ({}) given is not less than ({})".format(text, excluded_value))
        else:
            if not self._check_float(text):
                raise AssertionError("Value ({}) given is not a numeric or string value".format(text))
        
            if float(text) >= float(excluded_value):
                raise AssertionError("Value ({}) given is not less than ({})".format(text, excluded_value))
              
    def assertGreaterThanEqual(self, text, minimum_value, **params):
        if text is None:
            raise AssertionError("Value must be passed as a number or string")
        
        if isinstance(text, str):
            if text < minimum_value:
                raise AssertionError("Value ({}) given is less than the minimum allowed ({})".format(text, minimum_value))
        else:
            if not self._check_float(text):
                raise AssertionError("Value ({}) given is not a numeric or string value".format(text))
        
            if float(text) < float(minimum_value):
                raise AssertionError("Value ({}) given is less than the minimum allowed ({})".format(text, minimum_value))
        
    def assertGreaterThan(self, text, excluded_value, **params):
        if text is None:
            raise AssertionError("Value must be passed as a number or string")
        
        if isinstance(text, str):
            if text <= excluded_value:
                raise AssertionError("Value ({}) given is not greater than ({})".format(text, excluded_value))
        else:        
            if not self._check_float(text):
                raise AssertionError("Value ({}) given is not a numeric or string value".format(text))
        
            if float(text) <= float(excluded_value):
                raise AssertionError("Value ({}) given is not greater than ({})".format(text, excluded_value))
   
    def assertBetween(self, number, correct_values, **params):
        if isinstance(correct_values, str): 
            if ',' in correct_values:
                components = correct_values.split(',')
                minimum_value = components[0]
                maximum_value = components[1]
            else:
                AssertionError("Between needs multiple values, one ({}) given".format(correct_values))
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
            raise AssertionError("Value must be passed as a alpha-numeric string: {}".format(value))
        
        if not re.search(pattern, value):
            raise AssertionError("Value ({}) given does not match pattern {}".format(value, pattern))
        
    def assertIMatch(self, value, pattern, **params):
        if not value or not isinstance(value, str):
            raise AssertionError("Value must be passed as a alpha-numeric string: {}".format(value))
        
        if not re.search(pattern, value, re.IGNORECASE):
            raise AssertionError("Value ({}) given does not match pattern {}".format(value, pattern))
    
    
    def _convert_date(self, date):
        date_obj = None
        
        def try_date_format(format):
            try:
                return datetime.strptime(date, format)
            except Exception as e:
                return None    
        
        
        if not date or not isinstance(date, str):
            raise AssertionError("Value ({}) must be passed as a date string".format(date))
        
        for format in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'):
            date_obj = try_date_format(format)
            if date_obj: break
        
        if not date_obj:
            raise AssertionError("Value ({}) must be passed as a date string".format(date))
        
        return date_obj        
        
        
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
        
    def assertAny(self, list1, list2, **params):
        if not isinstance(list1, (list, tuple)):
            list1 = [list1]
            
        if not isinstance(list2, (list, tuple)):
            list2 = [list2]
            
        intersection = [value for value in list2 if value in list1]
        
        if len(intersection) == 0:
            raise AssertionError("There are no matching values ({}) within {}".format(list2, list1))
        
    def assertAll(self, list1, list2, **params):
        if not isinstance(list1, (list, tuple)):
            list1 = [list1]
            
        if not isinstance(list2, (list, tuple)):
            list2 = [list2]
            
        intersection = [value for value in list2 if value in list1]
      
        if len(intersection) != len(list2):
            raise AssertionError("Not all values ({}) are contained within {}".format(list2, list1))
        
    def assertNone(self, list1, list2, **params):
        if not isinstance(list1, (list, tuple)):
            list1 = [list1]
            
        if not isinstance(list2, (list, tuple)):
            list2 = [list2]
            
        intersection = [value for value in list2 if value in list1]
        
        if len(intersection) != 0:
            raise AssertionError("Values ({}) exist within {}".format(list2, list1))
