from django.db import IntegrityError
from django.test import TestCase

from game.models import Player, Game
from game.tests.factories.game import GameFactory
from game.tests.factories.player import PlayerFactory


class PlayerTest(TestCase):
    def test_create_player(self):
        my_game = GameFactory()
        my_player = Player(name="The winning team", game=my_game)

        self.assertEqual(my_player.game.name, my_game.name)
        self.assertEqual(my_player.name, "The winning team")

    def test_unique_player_names_conflict(self):
        player1 = PlayerFactory()
        with self.assertRaises(IntegrityError):
            player2 = PlayerFactory(game=player1.game, name=player1.name)

    def test_unique_player_names_no_conflict(self):
        player1 = PlayerFactory()
        player2 = PlayerFactory(name=player1.name)
        player1.full_clean()
        player2.full_clean()
        self.assertTrue(player1 in Player.objects.all())
        self.assertTrue(player2 in Player.objects.all())

    def test_cannot_create_player_without_game(self):
        my_player = Player(name="The winning team")
        with self.assertRaises(IntegrityError):
            my_player.save()

    def test_delete_player_does_not_delete_game(self):
        my_player = PlayerFactory()
        my_game = my_player.game
        my_player.delete()
        self.assertTrue(my_player not in Player.objects.all())
        self.assertTrue(my_game in Game.objects.all())

    def test_delete_game_deletes_player(self):
        player = PlayerFactory()
        player.save()
        game = player.game
        game.delete()
        self.assertTrue(player not in Player.objects.all())
