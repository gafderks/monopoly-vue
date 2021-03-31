from django.urls import path
from game.views import JoinGame

urlpatterns = [
    path("join/", JoinGame, name="join_game"),
]
