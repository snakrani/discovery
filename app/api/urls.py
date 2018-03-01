from api import routers, views


router = routers.OptionalSlashRouter()

router.register(r'naics', views.NaicsViewSet)
router.register(r'setasides', views.SetAsideViewSet)
router.register(r'pools', views.PoolViewSet)
router.register(r'zones', views.ZoneViewSet)
router.register(r'vendors', views.VendorViewSet)
router.register(r'contracts', views.ContractViewSet)
#router.register(r'metadata', views.MetadataViewSet)

urlpatterns = router.urls
