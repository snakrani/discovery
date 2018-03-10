

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
            return self.action_serializers[self.action]
        except (KeyError, AttributeError):
            return super(SerializerViewSetMixin, self).get_serializer_class()
