from discovery.utils import check_api_test

from rest_framework.exceptions import ParseError

from api.pagination import TestResultSetPagination, ResultNoPagination


class FilterViewSetMixin(object):
    
    action_filters = {}
    filter_backends = ()
    
    def get_filter_classes(self):
        try:
            filters = self.action_filters[self.action]
                        
            if isinstance(filters, str):
                filters = self.action_filters[filters]
            
            return filters
        
        except (KeyError, AttributeError):
            return ()
    
    def filter_queryset(self, queryset):
        self.filter_backends = self.get_filter_classes()
        return super(FilterViewSetMixin, self).filter_queryset(queryset)


class PaginationViewSetMixin(object):
    
    @property
    def paginator(self):
        page = self._get_query_param('page')
        count = self._get_query_param('count')
        
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            elif check_api_test(self.request):
                self._paginator = TestResultSetPagination()
            elif self.bypass_pagination and not self._use_pagination(page):
                self._paginator = ResultNoPagination()
            else:
                self._validate_page_count(count)
                self._paginator = self.pagination_class()
        
        return self._paginator
    
    
    def _validate_page_count(self, count):
        if self.bypass_pagination:
            count_options = [0, 5, 10, 20, 50, 100]
        else:
            count_options = [5, 10, 20, 50, 100]
        
        if count and int(count) not in count_options:
            raise ParseError("Paging count {} is not valid.  Choose from: {}".format(count, ", ".join(str(x) for x in count_options)))
    
    def _use_pagination(self, page):
        if page and int(page) == 0:
            return False
        return True
    
    
    def _get_query_param(self, name):
        if self.request and name in self.request.query_params:
            return self.request.query_params[name]
        return None
        


class SerializerViewSetMixin(object):
    
    action_serializers = {}
       
    def get_serializer_class(self):
        try:
            if check_api_test(self.request):
                if 'test' in self.action_serializers:
                    return self.action_serializers['test']
                else:
                    raise AttributeError()
            else:
                return self.action_serializers[self.action]
        
        except (KeyError, AttributeError):
            return None
