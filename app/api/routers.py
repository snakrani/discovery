from django.conf.urls import url

from rest_framework.routers import SimpleRouter, Route


class DiscoveryAPIRouter(SimpleRouter):
    
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Values route.
        Route(
            url=r'^{prefix}/values/{field_lookup}{trailing_slash}$',
            mapping={
                'get': 'values'
            },
            name='{basename}-values',
            initkwargs={'suffix': 'Values'}
        ),
        # Count route.
        Route(
            url=r'^{prefix}/count/{field_lookup}{trailing_slash}$',
            mapping={
                'get': 'count'
            },
            name='{basename}-count',
            initkwargs={'suffix': 'Count'}
        )
    ]
    
    def __init__(self):
        self.trailing_slash = '/?'
        super(SimpleRouter, self).__init__()
    
        
    def get_field_lookup_regex(self, viewset, lookup_prefix=''):
        base_regex = '(?P<{lookup_prefix}field_lookup>{lookup_value})'
        lookup_value = getattr(viewset, 'lookup_value_regex', '[^/.]+')
        
        return base_regex.format(
            lookup_prefix=lookup_prefix,
            lookup_value=lookup_value
        )
    
        
    def get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        ret = []

        for prefix, viewset, basename in self.registry:
            lookup = self.get_lookup_regex(viewset)
            field_lookup = self.get_field_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    field_lookup=field_lookup,
                    trailing_slash=self.trailing_slash
                )

                if not prefix and regex[:2] == '^/':
                    regex = '^' + regex[2:]

                initkwargs = route.initkwargs.copy()
                initkwargs.update({
                    'basename': basename,
                })

                view = viewset.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                ret.append(url(regex, view, name=name))

        return ret
