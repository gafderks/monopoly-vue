from django.db import models

from game.models.game import Game


class Player(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "game"], name="unique_player_names")
        ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
