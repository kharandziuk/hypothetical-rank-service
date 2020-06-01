from django.views.generic.list import ListView
from rest_framework import viewsets

from matches import models, serializers


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
