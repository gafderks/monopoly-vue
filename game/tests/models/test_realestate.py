from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from game.models import RealEstate, Game
from game.tests.factories.game import GameFactory
from game.tests.factories.realestate import RealEstateFactory


class RealEstateTest(TestCase):
    def test_create_realestate(self):
        game = GameFactory()
        estate = RealEstate(
            game=game,
            name="Kalverstraat",
            image="https://picsum.photos/200/300",
            purchase_price=Decimal("45.52"),
            rent_price=Decimal("33.90"),
        )
        estate.full_clean()
        estate.save()
        self.assertTrue(estate in RealEstate.objects.all())
        self.assertEqual(estate.game, game)
        self.assertEqual(estate.name, "Kalverstraat")
        self.assertEqual(estate.image, "https://picsum.photos/200/300")
        self.assertEqual(estate.purchase_price, Decimal("45.52"))
        self.assertEqual(estate.rent_price, Decimal("33.90"))

    def test_unique_realestate_names_conflict(self):
        estate1 = RealEstateFactory()
        with self.assertRaises(IntegrityError):
            estate2 = RealEstateFactory(game=estate1.game, name=estate1.name)

    def test_unique_realestate_names_no_conflict(self):
        estate1 = RealEstateFactory()
        estate2 = RealEstateFactory(name=estate1.name)
        estate1.full_clean()
        estate2.full_clean()
        self.assertTrue(estate1 in RealEstate.objects.all())
        self.assertTrue(estate2 in RealEstate.objects.all())

    def test_cannot_create_realestate_without_game(self):
        estate = RealEstate(
            name="Kalverstraat",
            image="https://picsum.photos/200/300",
            purchase_price=45.5,
            rent_price=33.9,
        )
        with self.assertRaises(IntegrityError):
            estate.save()

    def test_delete_realestate_does_not_delete_game(self):
        estate = RealEstateFactory()
        my_game = estate.game
        estate.delete()
        self.assertTrue(estate not in RealEstate.objects.all())
        self.assertTrue(my_game in Game.objects.all())

    def test_delete_game_deletes_realestate(self):
        estate = RealEstateFactory()
        estate.save()
        game = estate.game
        game.delete()
        self.assertTrue(estate not in RealEstate.objects.all())
