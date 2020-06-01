from rest_framework import serializers

from django.utils.timezone import make_aware
from django.conf import settings

from . import models


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Match
        fields = (
            'id',
        )
