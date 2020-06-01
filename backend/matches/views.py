from django.views.generic.list import ListView
from rest_framework import viewsets
from django_filters import rest_framework as filters

from matches import models, serializers


class MatchFilter(filters.FilterSet):
    # title, tournament, state, date_start__gte and date_start_lte
    title = filters.CharFilter(field_name="title__name", lookup_expr="icontains")
    tournament = filters.CharFilter(
        field_name="tournament__name", lookup_expr="icontains"
    )
    datetime_start__gte = filters.DateTimeFilter(
        field_name="datetime_start", lookup_expr="gte"
    )
    datetime_start__lte = filters.DateTimeFilter(
        field_name="datetime_start", lookup_expr="lte"
    )

    class Meta:
        model = models.Match
        fields = [
            "title",
            "tournament",
            "state",
            "datetime_start__gte",
            "datetime_start__lte",
        ]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    filterset_class = MatchFilter
