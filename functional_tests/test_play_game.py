from unittest import skip

from .base import FunctionalTest, english


@english
@skip
class PlayGameTest(FunctionalTest):
    def setUp(self):
        super().setUp()

    def test_can_join_game(self):
        # Alice wants to join a game of monopoly by entering the link she received
        self.browser.get(self.live_server_url)
        self.assertIn("Levend Monopoly", self.browser.title)

        # She needs to enter the password that she has
        # Accidentally, she enters the wrong password

        # She is denied access

        # She enters the correct password and needs to enter a name for her team
        # She gets a suggestion for the name of her team

        # She gets an overview of the locations in the neighborhood
        self.fail("Finish the test!")
