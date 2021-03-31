import datetime
from decimal import Decimal
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.test import TestCase

from game.models import Transaction, Player, RealEstate
from game.tests.factories.player import PlayerFactory
from game.tests.factories.realestate import RealEstateFactory
from game.tests.factories.transaction import TransactionFactory


class TransactionTest(TestCase):
    def test_create_transaction_with_realestate(self):
        estate = RealEstateFactory()
        creditor = PlayerFactory(game=estate.game)
        debtor = PlayerFactory(game=estate.game)
        my_transaction = Transaction(
            real_estate=estate,
            creditor=creditor,
            debtor=debtor,
            amount=Decimal("12.90"),
        )
        my_transaction.full_clean()
        my_transaction.save()
        self.assertTrue(my_transaction in Transaction.objects.all())
        self.assertEqual(my_transaction.real_estate, estate)
        self.assertEqual(my_transaction.debtor, debtor)
        self.assertEqual(my_transaction.creditor, creditor)
        self.assertEqual(my_transaction.amount, Decimal("12.90"))

    def test_timestamp(self):
        estate = RealEstateFactory()
        creditor = PlayerFactory(game=estate.game)
        debtor = PlayerFactory(game=estate.game)
        mocked = datetime.datetime(2021, 3, 3, 0, 2, 3, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            my_transaction = Transaction(
                real_estate=estate,
                creditor=creditor,
                debtor=debtor,
                amount=Decimal("12.90"),
            )
            my_transaction.save()
            self.assertEqual(my_transaction.timestamp, mocked)

    def test_cannot_creditor_and_debtor_from_different_game(self):
        creditor = PlayerFactory()
        debtor = PlayerFactory()
        estate = RealEstateFactory(game=creditor.game)
        my_transaction = Transaction(
            creditor=creditor, debtor=debtor, real_estate=estate
        )
        with self.assertRaises(ValidationError):
            my_transaction.full_clean()

    def test_cannot_creditor_and_estate_from_different_game(self):
        creditor = PlayerFactory()
        debtor = PlayerFactory(game=creditor.game)
        estate = RealEstateFactory()
        my_transaction = Transaction(
            creditor=creditor, debtor=debtor, real_estate=estate
        )
        with self.assertRaises(ValidationError):
            my_transaction.full_clean()

    def test_cannot_creditor_debtor_and_estate_from_different_game(self):
        creditor = PlayerFactory()
        debtor = PlayerFactory()
        estate = RealEstateFactory()
        my_transaction = Transaction(
            creditor=creditor, debtor=debtor, real_estate=estate
        )
        with self.assertRaises(ValidationError):
            my_transaction.full_clean()

    def test_delete_transaction_does_not_delete_creditor(self):
        my_transaction = TransactionFactory()
        creditor = my_transaction.creditor
        my_transaction.delete()
        self.assertTrue(my_transaction not in Transaction.objects.all())
        self.assertTrue(creditor in Player.objects.all())

    def test_delete_transaction_does_not_delete_debtor(self):
        my_transaction = TransactionFactory()
        debtor = my_transaction.debtor
        my_transaction.delete()
        self.assertTrue(my_transaction not in Transaction.objects.all())
        self.assertTrue(debtor in Player.objects.all())

    def test_delete_transaction_does_not_delete_realestate(self):
        my_transaction = TransactionFactory()
        estate = my_transaction.real_estate
        my_transaction.delete()
        self.assertTrue(my_transaction not in Transaction.objects.all())
        self.assertTrue(estate in RealEstate.objects.all())

    def test_delete_game_deletes_transaction(self):
        my_transaction = TransactionFactory()
        my_transaction.save()
        game = my_transaction.creditor.game
        game.delete()
        self.assertTrue(my_transaction not in Transaction.objects.all())

    def test_delete_creditor_deletes_transaction(self):
        my_transaction = TransactionFactory()
        my_transaction.save()
        creditor = my_transaction.creditor
        creditor.delete()
        self.assertTrue(my_transaction not in Transaction.objects.all())

    def test_delete_debtor_deletes_transaction(self):
        my_transaction = TransactionFactory()
        my_transaction.save()
        debtor = my_transaction.debtor
        debtor.delete()
        self.assertTrue(my_transaction not in Transaction.objects.all())
