from matches import models

import factory


class TournamentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tournament

    name = factory.Sequence(lambda n: f"tournament{n}")


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Team

    name = factory.Sequence(lambda n: f"team{n}")
    source = factory.SubFactory("matches.factories.SourceFactory")


class TitleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Title

    name = factory.Sequence(lambda n: f"title{n}")


class ScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Score

    team = factory.SubFactory(TeamFactory)
    score = 3


class SourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Source

    name = factory.Sequence(lambda n: f"source{n}")


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Match

    tournament = factory.SubFactory(TournamentFactory)
    state = 1
    source = factory.SubFactory(SourceFactory)
    title = factory.SubFactory(TitleFactory)
    external_id = factory.Sequence(lambda n: f"ext_id{n}")

    @factory.post_generation
    def scores(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        for _ in range(2):
            ScoreFactory(match=self)
