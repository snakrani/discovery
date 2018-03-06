from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

from rest_framework.documentation import include_docs_urls

from vendors import views as vendors


admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    
    url(r'^api/', include('api.urls')),
    url(r'^docs/', include_docs_urls(title="Discovery API", public=True)),
    
    url(r'^results/$', TemplateView.as_view(template_name='pool.html')),
    url(r'^results/csv', vendors.PoolCSV, name="pool-csv"),
    
    url(r'^vendor/(?P<vendor_duns>\w+)/$', vendors.VendorView.as_view(template_name='vendor.html')),
    url(r'^vendor/(?P<vendor_duns>\w+)/csv/$', vendors.VendorCSV, name="vendor-csv"),
]
