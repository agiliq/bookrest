from django.urls import path

from rest_framework import routers

from .views import get_viewsets, BookrestApiListView

router = routers.SimpleRouter()
viewsets = get_viewsets()
for table_name, viewset_class in viewsets:
    router.register(table_name, viewset_class)

urlpatterns = [
    path('', BookrestApiListView.as_view()),
] + router.urls

