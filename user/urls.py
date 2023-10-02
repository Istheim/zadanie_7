from user.apps import UserConfig
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet

app_name = UserConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [

              ] + router.urls
