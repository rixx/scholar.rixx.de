from rest_framework import permissions, viewsets

from scholar.core.models import Card, Source, Tag, Topic

from .serializers import (
    CardSerializer,
    SourceSerializer,
    TagSerializer,
    TopicSerializer,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class TagViewSet(BaseViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    # TODO filter by search


class SourceViewSet(BaseViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    # TODO filter by search


class CardViewSet(BaseViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    # TODO filter by search


class TopicViewSet(BaseViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    lookup_field = "title"
    # TODO filter by search
