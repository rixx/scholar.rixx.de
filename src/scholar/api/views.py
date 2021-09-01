from rest_framework import decorators, permissions, viewsets
from rest_framework.response import Response

from scholar.core.models import Card, Source, Tag, Topic

from .serializers import (
    CardSerializer,
    FlatSourceSerializer,
    FlatTagSerializer,
    FlatTopicSerializer,
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


@decorators.api_view()
def search(request):
    """TODO: limit on private elements"""
    search_term = request.query_params.get("q").strip().lower()
    short = request.query_params.get("short").strip().lower() in ("true", "on", "yes")
    if not search_term:
        return Response({"results": []})

    results = []

    all_results = [
        (
            "topic",
            Topic.objects.filter(title__icontains=search_term),
            FlatTopicSerializer,
        ),
        (
            "source",
            Source.objects.filter(title__icontains=search_term),
            FlatSourceSerializer,
        ),
        ("tag", Tag.objects.filter(name__icontains=search_term), FlatTagSerializer),
    ]
    for model, qs, serializer_class in all_results:
        if short:
            qs = qs[:5]
        for serialized in serializer_class(qs, many=True).data:
            serialized["type"] = model
            results.append(serialized)
    return Response({"result": results})
