"""Testable rules for Mystery Island: The Lost Lighthouse.

No input() or print() calls belong here. The CLI in main.py handles those.
"""

from copy import deepcopy

STARTING_ENERGY = 5

ROUTES = {
    "Beach": {"north": "Jungle"},
    "Jungle": {"south": "Beach", "east": "Cave"},
    "Cave": {"west": "Jungle", "north": "Old Bridge"},
    "Old Bridge": {"south": "Cave", "north": "Lighthouse"},
    "Lighthouse": {"south": "Old Bridge"},
}

SCENES = {
    "Beach": "Waves crash against the shore. A trail leads north into the jungle.",
    "Jungle": "Vines hide a sturdy rope. The cave lies east; the beach is south.",
    "Cave": "A lantern rests on a stone ledge. A path leads north to an old bridge.",
    "Old Bridge": "The bridge sways over a deep ravine. A rope could make it safe.",
    "Lighthouse": "The beacon is dark. Only a lantern can relight it.",
}

ITEM_LOCATIONS = {"rope": "Jungle", "lantern": "Cave"}
DIRECTIONS = ("north", "south", "east", "west")


def new_game(name="Explorer"):
    """Return an independent player state for a fresh adventure."""
    cleaned = name.strip() if isinstance(name, str) else ""
    return {
        "name": cleaned or "Explorer",
        "location": "Beach",
        "energy": STARTING_ENERGY,
        "inventory": [],
        "game_over": False,
        "won": False,
        "quit": False,
    }


def reset_game(player):
    """Start over with the same name, but fresh energy and inventory."""
    return new_game(player["name"])


def normalize_command(command):
    """Make commands case-insensitive and tolerate leading/trailing spaces."""
    return command.strip().lower() if isinstance(command, str) else ""


def can_cross_bridge(player):
    """A rope is necessary to travel from the bridge to the lighthouse."""
    return "rope" in player["inventory"]


def can_light_beacon(player):
    """The beacon can only be lit at the lighthouse with both useful items."""
    return (
        player["location"] == "Lighthouse"
        and "lantern" in player["inventory"]
        and "rope" in player["inventory"]
        and player["energy"] > 0
        and not player["game_over"]
    )


def available_actions(player):
    """Return display labels and canonical commands for the current room."""
    if player["game_over"]:
        return []
    options = []
    for direction, destination in ROUTES[player["location"]].items():
        options.append((f"Go {direction} to {destination}", direction))
    for item, location in ITEM_LOCATIONS.items():
        if location == player["location"]:
            options.append((f"Pick up {item}", f"take {item}"))
    if player["location"] == "Lighthouse":
        options.append(("Light the beacon", "light"))
    options.extend(
        [
            ("Look around (free)", "look"),
            ("Check inventory (free)", "inventory"),
            ("Explore further (costs 1 energy)", "explore"),
            ("Quit", "quit"),
        ]
    )
    return options


def describe_location(player):
    """Describe the scene without changing game state."""
    return SCENES[player["location"]]


def apply_action(player, command):
    """Apply a command and return (new_player, message).

    This function never mutates the caller's state. Invalid or blocked actions
    keep the state unchanged, including energy and inventory.
    """
    state = deepcopy(player)
    action = normalize_command(command)

    if state["game_over"]:
        return state, "The game has ended. Start a new game to play again."

    if action in {"quit", "exit", "q"}:
        state["game_over"] = True
        state["quit"] = True
        return state, "You ended the adventure. Goodbye!"

    if action == "look":
        return state, describe_location(state)

    if action in {"inventory", "inv", "i"}:
        items = ", ".join(state["inventory"]) or "empty"
        return state, f"Your inventory: {items}."

    if action.startswith("take "):
        item = action[5:].strip()
        if item not in ITEM_LOCATIONS:
            return state, "You cannot take that item. Try a listed action."
        if state["location"] != ITEM_LOCATIONS[item]:
            return state, f"There is no {item} here."
        if item in state["inventory"]:
            return state, f"You already collected the {item}."
        state["inventory"].append(item)
        return state, f"You picked up the {item}!"

    if action == "light":
        if state["location"] != "Lighthouse":
            return state, "You must reach the lighthouse before lighting the beacon."
        if "lantern" not in state["inventory"]:
            return state, "You need the lantern to light the beacon."
        if "rope" not in state["inventory"]:
            return state, "You must secure the crossing with the rope first."
        if can_light_beacon(state):
            state["won"] = True
            state["game_over"] = True
            return state, "VICTORY! The beacon shines. The rescue boat finds you!"
        return state, "The beacon cannot be lit yet."

    if action == "explore":
        state["energy"] = max(0, state["energy"] - 1)
        if state["energy"] == 0:
            state["game_over"] = True
            return state, "You explored too long and ran out of energy. GAME OVER!"
        return state, "You investigate the surroundings, but lose 1 energy."

    if action in DIRECTIONS:
        destination = ROUTES[state["location"]].get(action)
        if destination is None:
            return state, "You cannot go that way. Choose an available direction."
        if state["location"] == "Old Bridge" and destination == "Lighthouse":
            if not can_cross_bridge(state):
                return state, "The bridge is unsafe! Find the rope before crossing."
        state["location"] = destination
        state["energy"] = max(0, state["energy"] - 1)
        if state["energy"] == 0:
            state["game_over"] = True
            return state, f"You reach {destination}, but your energy runs out. GAME OVER!"
        return state, f"You travel to {destination}. (-1 energy)"

    return state, "Invalid command. Choose a menu number or an available command."
