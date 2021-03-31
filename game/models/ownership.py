from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.player import Player
from game.models.realestate import RealEstate


class Ownership(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)
    buy_timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.player.game != self.real_estate.game:
            raise ValidationError(
                _("Player and real estate must be from the same game.")
            )
