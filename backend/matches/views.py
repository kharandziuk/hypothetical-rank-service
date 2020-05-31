from django.views.generic.list import ListView

from matches import models

class MatchListView(ListView):
    model = models.Match
    paginate_by = 100

    def get_context_data(self):
        super()
