from django.conf.urls import url

from api import routers, views


router = routers.DiscoveryAPIRouter()

router.register('naics', views.NaicsViewSet)
router.register('psc', views.PscViewSet)
router.register('setasides', views.SetAsideViewSet)
router.register('pools', views.PoolViewSet)
router.register('zones', views.ZoneViewSet)
router.register('vendors', views.VendorViewSet)
router.register('contracts', views.ContractViewSet)

urlpatterns = [
    url(r'^keywords/$', views.ListKeywordView.as_view()),
    url(r'^metadata/$', views.ListMetadataView.as_view())
]
urlpatterns += router.urls
