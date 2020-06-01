from django.db import models
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


class MatchManager(models.Manager):
    def from_msg(self, msg):
        source, _ = Source.objects.get_or_create(
            name=msg['source']
        )
        msg_data=msg['data']
        if type(msg_data['tournament']) == str:
            tournament, _ = Tournament.objects.get_or_create(
                name=msg_data['tournament'],
                source=source
            )
        elif type(msg_data['tournament']) == dict:
            tournament, _ = Tournament.objects.update_or_create(
                external_id=msg_data['id'], source=source,
                defaults={"name": msg_data['tournament']['name']}
            )
        else:
            assert False
        for team_data in msg_data['teams']:
            team, _ = Team.objects.update_or_create(
                external_id=team_data['id'],
                source=source,
                defaults = { 'name': team_data['name'] }
            )
        title, _ = Title.objects.get_or_create(
            name=msg_data['title']
        )
        match, _ = self.update_or_create(
            source=source,
            external_id=msg_data['id'],
            defaults=dict(
                url=msg_data['url'],
                title=title,
                tournament=tournament,
                datetime_start=make_aware(parse_datetime(
                    msg_data['date_start_text'],
                )),
                bestof=msg_data['bestof'],
                state=msg_data['state']
            )
        )
        for score_data in msg_data['scores']:
            team = Team.objects.get(
                source=source,
                external_id=score_data['team'],
            )
            Score.objects.update_or_create(
                team=team,
                match=match,
                defaults=dict(
                    score=score_data['score'],
                    is_winner=score_data['winner']
                )
            )
        return match


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, null=True)
    source = models.ForeignKey(
        'matches.Source',
        on_delete=models.CASCADE,
        null=True
    )


class Source(models.Model):
    name= models.CharField(max_length=255, unique=True)


class Match(models.Model):
    title = models.ForeignKey('matches.Title', on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    bestof = models.CharField(max_length=255, null=True)
    datetime_start = models.DateTimeField(null=True)
    bestof = models.CharField(max_length=255, null=True)
    state = models.IntegerField()
    external_id = models.CharField(max_length=255, unique=True)

    source = models.ForeignKey(
        'matches.Source',
        on_delete=models.CASCADE,
    )

    objects = MatchManager()


class Title(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Score(models.Model):
    name = models.CharField(max_length=255)
    is_winner= models.BooleanField(null=True, blank=True)
    match = models.ForeignKey(
        'matches.Match',
        on_delete=models.CASCADE,
        related_name='scores'
    )
    team = models.ForeignKey(
        'matches.Team',
        on_delete=models.CASCADE,
        related_name='scores'
    )
    score = models.IntegerField(null=True, blank=True)

class Team(models.Model):
    name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255)
    source=models.ForeignKey(
        'matches.Source',
        on_delete=models.CASCADE,
    )
