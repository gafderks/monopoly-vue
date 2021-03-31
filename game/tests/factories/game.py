import factory

from game.models import Game


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    name = factory.Faker("company")
