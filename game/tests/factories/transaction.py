import factory

from game.models import Transaction
from game.tests.factories.player import PlayerFactory
from game.tests.factories.realestate import RealEstateFactory


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    creditor = factory.SubFactory(PlayerFactory)
    debtor = factory.SubFactory(
        PlayerFactory, game=factory.SelfAttribute("..creditor.game")
    )
    real_estate = factory.SubFactory(
        RealEstateFactory, game=factory.SelfAttribute("..creditor.game")
    )
    amount = factory.Faker("pydecimal", positive=True, max_value=999.0, right_digits=2)
