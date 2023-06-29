
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('variaciones',views.VariacionViewSet,basename="variaciones")



urlpatterns = router.urls