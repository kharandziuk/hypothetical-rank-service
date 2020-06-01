from django.urls import path

from matches import views

app_name = "matches"

urlpatterns = [
    path("", views.MatchViewSet.as_view(dict(get="list", post="create")), name="list"),
    path("<int:pk>", views.MatchViewSet.as_view(dict(get="retrieve")), name="detail"),
]
