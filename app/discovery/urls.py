from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles import views
from django.views.generic import TemplateView

from api import urls as api_urls
from vendors.views import VendorView, PoolCSV, VendorCSV


admin.autodiscover()


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include(api_urls)),
    #url(r'^docs/', get_swagger_view(title='Discovery API')),
    url(r'^results/$', TemplateView.as_view(template_name='pool.html')),
    url(r'^results/csv', PoolCSV, name="pool-csv"),
    url(r'^vendor/(?P<vendor_duns>\w+)/$', VendorView.as_view(template_name='vendor.html')),
    url(r'^vendor/(?P<vendor_duns>\w+)/csv/$', VendorCSV, name="vendor-csv"),   
    url(r'^admin/', admin.site.urls)    
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
