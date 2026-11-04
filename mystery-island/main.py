"""Command-line interface for Mystery Island: The Lost Lighthouse."""

from game import apply_action, available_actions, describe_location, new_game


TITLE = "MYSTERY ISLAND: THE LOST LIGHTHOUSE"


def choose_command(player, raw_choice):
    """Translate menu numbers into commands; allow direct typed commands too."""
    cleaned = raw_choice.strip().lower()
    options = available_actions(player)
    if cleaned.isdecimal():
        number = int(cleaned)
        if 1 <= number <= len(options):
            return options[number - 1][1]
        return ""  # An out-of-range number is an invalid command.
    return cleaned


def show_menu(player):
    """Display where the player is and the available actions."""
    print(f"\nLocation: {player['location']} | Energy: {player['energy']}/{5}")
    print(describe_location(player))
    for number, (label, _command) in enumerate(available_actions(player), start=1):
        print(f"  {number}. {label}")


def ask_replay():
    """Return True to play again, False to stop; reject other responses."""
    while True:
        try:
            answer = input("\nPlay again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return False
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def main():
    """Run the game and optionally replay with a fresh player state."""
    print("=" * len(TITLE))
    print(TITLE)
    print("=" * len(TITLE))
    print("Restore the beacon before your energy runs out!")
    print("Moves cost 1 energy. Collect the rope and lantern for free.")
    print("'Explore further' costs 1 energy. Invalid commands are free.")
    print("Type a menu number or a command (e.g. north, take rope, quit).")
    try:
        name = input("\nWhat is your name, explorer? ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        return

    while True:
        player = new_game(name)
        print(f"\nWelcome to Mystery Island, {player['name']}!")

        while not player["game_over"]:
            show_menu(player)
            try:
                raw_choice = input("Choose your action: ")
            except (EOFError, KeyboardInterrupt):
                raw_choice = "quit"
                print("\nInput closed. Ending the adventure.")
            command = choose_command(player, raw_choice)
            player, message = apply_action(player, command)
            print(message)

        if player["won"]:
            print(f"Well done, {player['name']}! You escaped Mystery Island.")
        elif not player["quit"]:
            print("The rescue boat cannot find you without the beacon.")

        if not ask_replay():
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
