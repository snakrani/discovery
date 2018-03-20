from discovery.utils import check_api_test


class FilterViewSetMixin(object):
    
    action_filters = {}
    filter_backends = ()
    
    def get_filter_classes(self):
        try:
            return self.action_filters[self.action]
        except (KeyError, AttributeError):
            return ()
    
    def filter_queryset(self, queryset):
        self.filter_backends = self.get_filter_classes()            
        return super(FilterViewSetMixin, self).filter_queryset(queryset)


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
            return super(SerializerViewSetMixin, self).get_serializer_class()
