import datetime
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from game.models import Ownership, Game, Player, RealEstate
from game.tests.factories.ownership import OwnershipFactory
from game.tests.factories.player import PlayerFactory
from game.tests.factories.realestate import RealEstateFactory


class OwnershipTest(TestCase):
    def test_create_ownership(self):
        estate = RealEstateFactory()
        player = PlayerFactory(game=estate.game)
        my_ownership = Ownership(real_estate=estate, player=player)
        my_ownership.full_clean()
        my_ownership.save()
        self.assertTrue(my_ownership in Ownership.objects.all())
        self.assertEqual(my_ownership.real_estate, estate)
        self.assertEqual(my_ownership.player, player)

    def test_buy_timestamp(self):
        estate = RealEstateFactory()
        player = PlayerFactory(game=estate.game)
        mocked = datetime.datetime(2021, 3, 3, 0, 2, 3, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            my_ownership = Ownership(real_estate=estate, player=player)
            my_ownership.save()
            self.assertEqual(my_ownership.buy_timestamp, mocked)

    def test_cannot_create_ownership_without_player(self):
        ownership = Ownership(real_estate=RealEstateFactory())
        with self.assertRaises(IntegrityError):
            ownership.save()

    def test_cannot_create_ownership_without_realestate(self):
        ownership = Ownership(player=PlayerFactory())
        with self.assertRaises(IntegrityError):
            ownership.save()

    def test_delete_ownership_does_not_delete_game_player_or_realestate(self):
        ownership = OwnershipFactory()
        player = ownership.player
        real_estate = ownership.real_estate
        game = ownership.player.game
        self.assertEqual(player.game, real_estate.game)
        ownership.delete()
        self.assertTrue(ownership not in Ownership.objects.all())
        self.assertTrue(game in Game.objects.all())
        self.assertTrue(player in Player.objects.all())
        self.assertTrue(real_estate in RealEstate.objects.all())

    def test_cannot_player_and_realestate_from_different_game(self):
        player = PlayerFactory()
        estate = RealEstateFactory()
        my_ownership = Ownership(player=player, real_estate=estate)
        with self.assertRaises(ValidationError):
            my_ownership.full_clean()

    def test_delete_player_deletes_ownership(self):
        ownership = OwnershipFactory()
        ownership.save()
        player = ownership.player
        player.delete()
        self.assertTrue(ownership not in Ownership.objects.all())

    def test_delete_realestate_deletes_ownership(self):
        ownership = OwnershipFactory()
        ownership.save()
        realestate = ownership.real_estate
        realestate.delete()
        self.assertTrue(ownership not in Ownership.objects.all())

    def test_delete_game_deletes_ownership(self):
        ownership = OwnershipFactory()
        ownership.save()
        game = ownership.player.game
        game.delete()
        self.assertTrue(ownership not in Ownership.objects.all())
