# urls.py
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r"", TaskViewSet)

urlpatterns = router.urls
