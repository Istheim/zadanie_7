from payment.apps import PaymentConfig
from rest_framework.routers import DefaultRouter

from payment.views import PaymentViewSet

app_name = PaymentConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = urlpatterns = router.urls
