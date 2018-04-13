from django.conf.urls import url

from api import routers, views


router = routers.OptionalSlashRouter()

router.register(r'naics', views.NaicsViewSet)
router.register(r'psc', views.PscViewSet)
router.register(r'setasides', views.SetAsideViewSet)
router.register(r'pools', views.PoolViewSet)
router.register(r'zones', views.ZoneViewSet)
router.register(r'vendors', views.VendorViewSet)
router.register(r'contracts', views.ContractViewSet)

urlpatterns = [
    url(r'^metadata/$', views.ListMetadataView.as_view()),
]

urlpatterns += router.urls
