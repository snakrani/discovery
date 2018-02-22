from django.conf.urls import include, url
from django.views.decorators.cache import cache_page
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    url(r'^naics/$', cache_page(60*60*48)(views.ListNaics.as_view())),
    url(r'^pools/$', cache_page(60*60*48)(views.ListPools.as_view())),
    url(r'^zones/$', cache_page(60*60*48)(views.ListZones.as_view())),
    
    url(r'^vendors/$', cache_page(60*60*24)(views.ListVendors.as_view())),
    url(r'^vendor/(?P<duns>\w+)', cache_page(60*60*24)(views.GetVendor.as_view())),
    
    url(r'^contracts/$', cache_page(60*60*24)(views.ListContracts.as_view())),
    
    url(r'^metadata/$', cache_page(60*60*24)(views.MetadataView.as_view())),
]

urlpatterns = format_suffix_patterns(urlpatterns)
