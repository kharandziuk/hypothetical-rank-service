import json
import datetime
from matches import models
import pytest

from django.conf import settings

pytestmark = pytest.mark.django_db


def test_can_properly_handle_message_1():
    with open(settings.BASE_DIR / 'artifacts' / 'message1.json') as file_with_message:
        msg = json.loads(file_with_message.read())
        match = models.Match.objects.from_msg(msg)
        assert match.url == "https://www.source1.org/matches/1/"
        assert match.title.name == 'Overcooked'
        assert match.bestof == "3"
        assert match.datetime_start != None
        tournament = match.tournament
        assert tournament.name == "Overbayes Season 1"
        score1, score2 = match.scores.all()
        assert score1.team.name == 'Bayes Esports Team 1'
        assert score1.score == None
        assert score2.team.name == 'Bayes Team 2'
        assert score1.score == None

def test_can_handle_all_the_messages():
    for x in range(1, 5):
        path = settings.BASE_DIR / 'artifacts' / f'message{x}.json'
        with open(path) as file_with_message:
            msg = json.loads(file_with_message.read())
            match = models.Match.objects.from_msg(msg)
    assert models.Match.objects.count() == 3
