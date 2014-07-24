from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^vendors/$', 'api.views.vendor_list'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
