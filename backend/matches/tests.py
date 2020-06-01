import json
import datetime
from matches import models, factories
import pytest

from django.urls import reverse

from django.conf import settings

pytestmark = pytest.mark.django_db


def test_match_empty_list(client):
    url = reverse('matches:list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


def test_match_empty_list(client):
    match = factories.MatchFactory()
    url = reverse('matches:list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [dict(
        id=match.id
    )]


def test_match_detail(client):
    match = factories.MatchFactory()
    url = reverse('matches:detail', args=[match.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == dict(
        id=match.id
    )


