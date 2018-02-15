from rest_framework import routers
from tests.app.api import OfficeViewSet, IssueViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('offices', OfficeViewSet)
router.register('issues', IssueViewSet)
router.register('users', UserViewSet)

urlpatterns = router.urls