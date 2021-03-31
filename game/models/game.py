import secrets

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    name = models.CharField(max_length=250)
    admin_pin = models.CharField(
        max_length=20, editable=False, default=secrets.token_urlsafe()
    )
    player_pin = models.CharField(
        max_length=20, editable=False, default=secrets.token_urlsafe()
    )

    def clean(self):
        if self.admin_pin == self.player_pin:
            raise ValidationError(_("Admin pin and player pin must be different."))
