from django.db import models

from game.models.game import Game


class RealEstate(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "game"], name="unique_realestate_names"
            )
        ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.URLField()

    purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    rent_price = models.DecimalField(max_digits=5, decimal_places=2)
