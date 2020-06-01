import json
import datetime
from matches import models, factories
import pytest

from django.urls import reverse

from django.conf import settings
from django.utils.http import urlencode

pytestmark = pytest.mark.django_db


def reverseq(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return u"%s?%s" % (url, urlencode(query_kwargs))

    return url


def test_match_empty_list(client):
    url = reverse("matches:list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


def test_match_list(client):
    match = factories.MatchFactory()
    url = reverse("matches:list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()[0]["id"] == match.id
    assert response.json()[0]["scores"] == [
        dict(score=3, team_name="team0"),
        dict(score=3, team_name="team1"),
    ]


def test_match_detail(client):
    match = factories.MatchFactory()
    url = reverse("matches:detail", args=[match.id])
    response = client.get(url)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()["id"] == match.id


def test_can_filter_by_match(client):
    title = factories.TitleFactory(name="this")
    searched_match = factories.MatchFactory(title=title)
    other_match = factories.MatchFactory()
    url = reverseq("matches:list", query_kwargs=dict(title="this"))
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == searched_match.id
