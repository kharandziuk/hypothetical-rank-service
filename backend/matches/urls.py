from django.urls import path

from matches import views

app_name = "matches"

urlpatterns = [
    path('', views.MatchListView.as_view(), name='matches-list'),
]
