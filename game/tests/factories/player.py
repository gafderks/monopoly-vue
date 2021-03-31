import factory

from game.models import Player
from game.tests.factories.game import GameFactory


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    name = factory.Faker("first_name")
    game = factory.SubFactory(GameFactory)
