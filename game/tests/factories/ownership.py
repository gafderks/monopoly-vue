import factory

from game.models import Ownership
from game.tests.factories.player import PlayerFactory
from game.tests.factories.realestate import RealEstateFactory


class OwnershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ownership

    player = factory.SubFactory(PlayerFactory)
    real_estate = factory.SubFactory(
        RealEstateFactory, game=factory.SelfAttribute("..player.game")
    )
