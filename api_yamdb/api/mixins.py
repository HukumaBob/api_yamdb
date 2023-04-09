from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin


class CommonCreateListDestroyViewset(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass