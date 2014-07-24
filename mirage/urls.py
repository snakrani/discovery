from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import urls as api_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mirage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(api_urls)),
    url(r'^admin/', include(admin.site.urls)),
)

