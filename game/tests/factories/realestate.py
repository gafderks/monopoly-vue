import factory

from game.models import RealEstate
from game.tests.factories.game import GameFactory


class RealEstateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RealEstate

    name = factory.Faker("street_name")
    game = factory.SubFactory(GameFactory)
    image = factory.Faker("image_url")

    purchase_price = factory.Faker(
        "pydecimal", positive=True, max_value=999.0, right_digits=2
    )
    rent_price = factory.Faker(
        "pydecimal", positive=True, max_value=999.0, right_digits=2
    )
