from rest_framework import serializers

from django.utils.timezone import make_aware
from django.conf import settings

from . import models


class ScoreSerilizer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name")

    class Meta:
        model = models.Score
        fields = ("score", "team_name")


class MatchSerializer(serializers.ModelSerializer):
    scores = ScoreSerilizer(many=True)

    class Meta:
        model = models.Match
        fields = ("id", "scores")
