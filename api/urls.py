from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = patterns('',
    url(r'^vendors/$', views.ListVendors.as_view()),
    url(r'^vendor/(?P<duns>\w+)', views.GetVendor.as_view()),
    url(r'^naics/$', views.ListNaics.as_view()),
    url(r'^contracts/$', views.ListContracts.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
