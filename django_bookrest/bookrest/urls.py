from rest_framework import routers

from .views import get_viewsets

router = routers.SimpleRouter()
viewsets = get_viewsets()
for table_name, viewset_class in viewsets:
    router.register(table_name, viewset_class)

urlpatterns = router.urls
