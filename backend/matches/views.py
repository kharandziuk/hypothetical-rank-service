from django.views.generic.list import ListView
from rest_framework import viewsets
from django_filters import rest_framework as filters

from matches import models, serializers


class MatchFilter(filters.FilterSet):
     # title, tournament, state, date_start__gte and date_start_lte
    title = filters.CharFilter(
        field_name="title__name",
        lookup_expr='icontains'
    )

    class Meta:
        model = models.Match
        fields = ['title']


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    filterset_class = MatchFilter
