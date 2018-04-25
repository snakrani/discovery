from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from uaa_client.decorators import staff_login_required

from vendors import views as vendors


admin.autodiscover()
admin.site.login = staff_login_required(admin.site.login)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('uaa_client.urls')),
    
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    
    url(r'^api/', include('api.urls')),
    url(r'^api/', include_docs_urls(title="Discovery API", public=True)),
    url(r'^docs/', RedirectView.as_view(url='/api', permanent=False)),
    url(r'^developers?/', RedirectView.as_view(url='/api', permanent=False)),
        
    url(r'^results/$', TemplateView.as_view(template_name='pool.html')),
    url(r'^results/csv', vendors.PoolCSV, name="pool-csv"),
    
    url(r'^vendor/(?P<vendor_duns>\w+)/$', vendors.VendorView.as_view(template_name='vendor.html')),
    url(r'^vendor/(?P<vendor_duns>\w+)/csv/$', vendors.VendorCSV, name="vendor-csv"),
]
