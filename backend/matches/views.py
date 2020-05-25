from django.views.generic.list import ListView

from matches import models

class MatchListView(ListView):
    model = models.Match
