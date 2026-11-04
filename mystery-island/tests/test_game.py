"""Acceptance and edge-case tests for the adventure's game rules."""

import unittest

from game import (
    STARTING_ENERGY,
    apply_action,
    available_actions,
    can_cross_bridge,
    can_light_beacon,
    new_game,
    normalize_command,
    reset_game,
)


class MysteryIslandTests(unittest.TestCase):
    def test_new_game_starts_with_five_energy_on_beach(self):
        player = new_game("Ada")
        self.assertEqual(player["name"], "Ada")
        self.assertEqual(player["location"], "Beach")
        self.assertEqual(player["energy"], STARTING_ENERGY)
        self.assertEqual(player["inventory"], [])
        self.assertFalse(player["game_over"])

    def test_invalid_command_does_not_change_state(self):
        player = new_game()
        updated, message = apply_action(player, "banana")
        self.assertEqual(updated, player)
        self.assertIn("Invalid", message)

    def test_legal_move_changes_location_and_costs_one_energy(self):
        updated, _ = apply_action(new_game(), "north")
        self.assertEqual(updated["location"], "Jungle")
        self.assertEqual(updated["energy"], 4)

    def test_wrong_direction_is_rejected_without_cost(self):
        player = new_game()
        updated, message = apply_action(player, "west")
        self.assertEqual(updated, player)
        self.assertIn("cannot", message)

    def test_rope_can_be_collected_only_once(self):
        jungle, _ = apply_action(new_game(), "north")
        jungle, _ = apply_action(jungle, "take rope")
        repeated, message = apply_action(jungle, "take rope")
        self.assertEqual(repeated["inventory"], ["rope"])
        self.assertEqual(repeated["energy"], jungle["energy"])
        self.assertIn("already", message)

    def test_bridge_cannot_be_crossed_without_rope(self):
        player = new_game()
        player["location"] = "Old Bridge"
        blocked, message = apply_action(player, "north")
        self.assertEqual(blocked, player)
        self.assertFalse(can_cross_bridge(player))
        self.assertIn("rope", message)

    def test_lighthouse_cannot_be_lit_without_lantern(self):
        player = new_game()
        player["location"] = "Lighthouse"
        player["inventory"] = ["rope"]
        blocked, message = apply_action(player, "light")
        self.assertEqual(blocked, player)
        self.assertIn("lantern", message)

    def test_correct_items_and_location_win(self):
        player = new_game()
        player["location"] = "Lighthouse"
        player["energy"] = 1
        player["inventory"] = ["rope", "lantern"]
        self.assertTrue(can_light_beacon(player))
        won, message = apply_action(player, "light")
        self.assertTrue(won["won"])
        self.assertTrue(won["game_over"])
        self.assertIn("VICTORY", message)

    def test_fifth_energy_use_causes_loss_and_never_negative(self):
        player = new_game()
        for _ in range(5):
            player, _ = apply_action(player, "explore")
        self.assertEqual(player["energy"], 0)
        self.assertTrue(player["game_over"])
        self.assertFalse(player["won"])

    def test_replay_resets_energy_location_and_inventory(self):
        player = new_game("Ada")
        player, _ = apply_action(player, "north")
        player, _ = apply_action(player, "take rope")
        replayed = reset_game(player)
        self.assertEqual(replayed["name"], "Ada")
        self.assertEqual(replayed["location"], "Beach")
        self.assertEqual(replayed["energy"], 5)
        self.assertEqual(replayed["inventory"], [])
        self.assertIsNot(replayed["inventory"], player["inventory"])

    def test_whitespace_and_uppercase_command_is_valid(self):
        player, _ = apply_action(new_game(), "  NORTH  ")
        self.assertEqual(player["location"], "Jungle")
        self.assertEqual(normalize_command(" EXIT "), "exit")

    def test_player_state_is_not_mutated(self):
        original = new_game()
        new_state, _ = apply_action(original, "north")
        self.assertEqual(original["energy"], 5)
        self.assertEqual(original["location"], "Beach")
        self.assertNotEqual(original, new_state)

    def test_collect_lantern_only_in_cave(self):
        player = new_game()
        blocked, _ = apply_action(player, "take lantern")
        self.assertEqual(blocked, player)
        player, _ = apply_action(player, "north")
        player, _ = apply_action(player, "east")
        player, _ = apply_action(player, "take lantern")
        self.assertIn("lantern", player["inventory"])
        self.assertEqual(player["energy"], 3)

    def test_winning_path_end_to_end(self):
        player = new_game("Ada")
        for action in ("north", "take rope", "east", "take lantern", "north", "north", "light"):
            player, _ = apply_action(player, action)
        self.assertTrue(player["won"])
        self.assertTrue(player["game_over"])
        self.assertEqual(player["energy"], 1)
        self.assertEqual(player["location"], "Lighthouse")

    def test_cannot_move_after_game_over(self):
        player, _ = apply_action(new_game(), "quit")
        unchanged, message = apply_action(player, "north")
        self.assertEqual(unchanged, player)
        self.assertIn("ended", message)

    def test_no_win_without_visiting_lighthouse(self):
        player = new_game()
        player["inventory"] = ["rope", "lantern"]
        self.assertFalse(can_light_beacon(player))
        updated, message = apply_action(player, "light")
        self.assertFalse(updated["won"])
        self.assertIn("lighthouse", message)

    def test_quit_does_not_count_as_loss(self):
        player, _ = apply_action(new_game(), " EXIT ")
        self.assertTrue(player["game_over"])
        self.assertTrue(player["quit"])
        self.assertEqual(player["energy"], 5)
        self.assertFalse(player["won"])

    def test_blocked_move_and_invalid_item_cost_no_energy(self):
        player = new_game()
        for action in ("take rope", "take pineapple", "west", "xyz"):
            current, _ = apply_action(player, action)
            self.assertEqual(current, player)

    def test_all_five_locations_present(self):
        self.assertEqual(
            {"Beach", "Jungle", "Cave", "Old Bridge", "Lighthouse"},
            {"Beach"} | {
                dest for source in ("Beach", "Jungle", "Cave", "Old Bridge", "Lighthouse")
                for label, dest in self._destinations(source)
            },
        )

    @staticmethod
    def _destinations(location):
        player = new_game()
        player["location"] = location
        return [
            (label, label.split(" to ")[-1])
            for label, _ in available_actions(player)
            if label.startswith("Go ")
        ]


if __name__ == "__main__":
    unittest.main()
