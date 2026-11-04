"""Tests for menu numbering and the command-line experience."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from game import new_game
from main import choose_command, main


class CommandLineTests(unittest.TestCase):
    def test_menu_numeric_selection_for_first_move(self):
        player = new_game()
        self.assertEqual(choose_command(player, " 1 "), "north")

    def test_out_of_range_menu_number_is_invalid(self):
        player = new_game()
        self.assertEqual(choose_command(player, "999"), "")

    def test_game_win_through_cli(self):
        # At each location, the menu lists routes before items/actions.
        commands = [
            "Ada", "north", "take rope", "east", "take lantern",
            "north", "north", "light", "n",
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), redirect_stdout(output):
            main()
        self.assertIn("VICTORY!", output.getvalue())
        self.assertIn("Thanks for playing!", output.getvalue())

    def test_replay_uses_fresh_state_through_cli(self):
        commands = ["Ada", "quit", "y", "quit", "n"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), redirect_stdout(output):
            main()
        self.assertEqual(output.getvalue().count("Location: Beach | Energy: 5/5"), 2)


if __name__ == "__main__":
    unittest.main()
