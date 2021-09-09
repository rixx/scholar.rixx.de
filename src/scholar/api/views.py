from django.db import transaction
from django.db.models import Q
from django.http import Http404
from rest_framework import decorators, permissions, viewsets
from rest_framework.response import Response

from scholar.core.models import Card, Source, Tag, Topic

from .serializers import (
    CardSerializer,
    CardWriteSerializer,
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

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return getattr(self, "write_serializer_class", self.serializer_class)
        return self.serializer_class


class TagViewSet(BaseViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class SourceViewSet(BaseViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()


class CardViewSet(BaseViewSet):
    serializer_class = CardSerializer
    write_serializer_class = CardWriteSerializer
    queryset = Card.objects.all()

    @transaction.atomic()
    def create(self, *args, **kwargs):
        result = super().create(*args, **kwargs)
        return result


class TopicViewSet(BaseViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    lookup_field = "slug"

    def get_object(self):
        slug = self.kwargs["slug"].replace("_", " ")
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(
            Q(title_en__iexact=slug) | Q(title_de__iexact=slug)
        ).first()
        if not obj:
            raise Http404()
        return obj


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
            Topic.objects.filter(
                Q(title_en__icontains=search_term) |
                Q(title_de__icontains=search_term),
            ),
            FlatTopicSerializer,
        ),
        (
            "source",
            Source.objects.filter(
                Q(title__icontains=search_term)
                | Q(url__icontains=search_term)
                | Q(author__icontains=search_term)
            ),
            FlatSourceSerializer,
        ),
        (
            "tag",
            Tag.objects.filter(
                name_en__icontains=search_term,
                name_de__icontains=search_term,
            ),
            FlatTagSerializer,
        ),
    ]
    for model, qs, serializer_class in all_results:
        if short:
            qs = qs[:5]
        for serialized in serializer_class(qs, many=True).data:
            serialized["type"] = model
            results.append(serialized)
    return Response({"result": results})
