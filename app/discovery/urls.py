from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.documentation import include_docs_urls

from vendors import views as vendors
from contracts import views as contracts


urlpatterns = [
    # API related endpoints        
    url(r'^api/', include('api.urls')),
    url(r'^api/', include_docs_urls(title="Discovery API", public=True)),
    url(r'^api$', RedirectView.as_view(url='/api/', permanent=False)),
    url(r'^docs/?', RedirectView.as_view(url='/api/', permanent=False)),
    url(r'^developers?/?', RedirectView.as_view(url='/api/', permanent=False)),

    # Data export endpoints
    url(r'^csv/vendors', vendors.VendorCSV.as_view(), name="vendor-csv"),
    url(r'^csv/contracts/(?P<vendor_duns>\w+)', contracts.ContractCSV.as_view(), name="contract-csv"),

    # Frontend routes
    url(r'^404$', TemplateView.as_view(template_name='index.html')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^search.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^about.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^contracts.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^oasis.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^hcats.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^bmo.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^pss.*$', TemplateView.as_view(template_name='index.html')),
    url(r'^.*$', RedirectView.as_view(url='/404', permanent=False)),
]
