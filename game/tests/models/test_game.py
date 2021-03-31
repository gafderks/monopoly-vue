from django.core.exceptions import ValidationError
from django.test import TestCase

from game.models import Game
from game.tests.factories.game import GameFactory


class GameTest(TestCase):
    def test_create_game(self):
        my_game = Game(
            name="Super game",
        )

        self.assertEqual(my_game.name, "Super game")

    def test_different_pins(self):
        game = GameFactory(admin_pin="abc", player_pin="abc")
        with self.assertRaises(ValidationError):
            game.full_clean()
