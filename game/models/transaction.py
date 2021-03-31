from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.player import Player
from game.models.realestate import RealEstate


class Transaction(models.Model):
    creditor = models.ForeignKey(
        Player, blank=True, on_delete=models.CASCADE, related_name="credits"
    )
    debtor = models.ForeignKey(
        Player, blank=True, on_delete=models.CASCADE, related_name="debits"
    )
    real_estate = models.ForeignKey(RealEstate, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if not (self.creditor.game == self.debtor.game == self.real_estate.game):
            raise ValidationError(
                _("Creditor, debtor and real estate must be from the same game.")
            )
