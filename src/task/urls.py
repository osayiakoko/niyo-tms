# urls.py
from rest_framework.routers import SimpleRouter
from .views import TaskViewSet

app_name = "task"

router = SimpleRouter(trailing_slash=False)
router.register(r"", TaskViewSet)

urlpatterns = router.urls
