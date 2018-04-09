from rest_framework import serializers, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .introspect import ConnectionToModels
from django.db import connections, models

BOOKREST_DB_NAME = "bookrest"

class BookrestApiListView(APIView):
    """
    Lists all the APIs which Bookrest will enable
    """

    def get(self, request, format=None):
        models = ConnectionToModels(connections[BOOKREST_DB_NAME]).get_models()
        table_names = [
            {'name': model._meta.db_table,
             'objects_count': model.objects.count(),
             'url': reverse('{}-list'.format(model._meta.model_name), request=request)
            }
            for model in models]
        return Response(table_names)


def get_viewsets():
    """
    A list of two-tuples of (table_name, model)
    """
    models = ConnectionToModels(connections[BOOKREST_DB_NAME]).get_models()
    viewsets = ModelToDrf(models).get_viewsets()
    return zip([model._meta.db_table for model in models], viewsets)


class ModelToDrf:

    def __init__(self, models):
        self.models = models

    def get_viewsets(self):
        serializers = self.get_serializers()
        serializers_with_models = zip(self.models, serializers)
        return [
            self.get_viewset(model_class, serializer_class)
            for model_class, serializer_class in serializers_with_models
        ]

    def get_serializers(self):
        return [self.get_serializer(model_class) for model_class in self.models]

    @staticmethod
    def get_viewset(model_class, serializer_klass):
        searchable_field_name = [
            field.name
            for field in model_class._meta.get_fields()
            if ModelToDrf.is_textual_field(field)
        ]

        class ViewSet(viewsets.ModelViewSet):
            serializer_class = serializer_klass
            queryset = model_class.objects.all()
            filter_backends = (SearchFilter,)
            search_fields = searchable_field_name

        return type("{}ViewSet".format(model_class._meta), (ViewSet,), {})

    @staticmethod
    def is_textual_field(field):
        return isinstance(field, models.TextField)

    @staticmethod
    def get_serializer(model_class):
        fields_name = ['url'] + [
            field.name
            for field in model_class._meta.get_fields()
        ]
        class Serializer(serializers.ModelSerializer):

            class Meta:
                model = model_class
                fields = fields_name

        return Serializer

