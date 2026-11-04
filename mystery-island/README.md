# Mystery Island: The Lost Lighthouse 🏝️

A beginner-friendly **Python command-line adventure** built for the Learn2Earn Easy Track. Find a rope and a lantern, cross the old bridge, and light the lighthouse before your energy runs out.

> **Development disclosure:** This version was generated with ChatGPT assistance to provide a runnable project quickly. The learner should study, test, modify, and explain it before representing it as independently built work. See `LEARNING_GUIDE.md` for a self-build plan.

## Requirements

- Python 3.9 or newer (uses **only the standard library**)
- A terminal/command prompt

## Run the game

```bash
python main.py
```

On some computers the command is `python3 main.py`.

You will be asked for your name. At each location, type a **menu number** or a **command** such as `north`, `take rope`, `inventory`, `look`, `explore`, `quit`, or `exit`.

## Rules

- Start at the **Beach** with **5 energy**, an empty inventory, and no items collected.
- Visit five locations: **Beach → Jungle → Cave → Old Bridge → Lighthouse**. Backtracking is possible.
- A legal move costs **1 energy**. Invalid/blocked commands and item pickups cost **0 energy**.
- Pick up the **rope** in the **Jungle** and the **lantern** in the **Cave**. Each can be collected only once.
- Crossing from **Old Bridge** to **Lighthouse** requires the rope.
- At the **Lighthouse**, the `light` action requires the lantern (and your rope).
- `explore` is optional and costs 1 energy; wasting energy may prevent rescue.
- Reaching **0 energy** causes an immediate loss, never negative energy.
- You can **quit** or **replay**. Replay starts with a completely fresh player state.
- Input such as ` NORTH ` is accepted. Invalid commands never reduce energy.

## Example winning path

Choose these commands, in order (after entering a name):

```text
north
 take rope
 east
 take lantern
 north
 north
 light
 n
```

The player arrives at the Lighthouse with **1 energy** and wins by lighting the beacon. The commands above may include spaces because the game strips surrounding whitespace.

## Example losing path

Enter `explore` five times while on the Beach. Your energy goes from **5 → 4 → 3 → 2 → 1 → 0**, and the game ends in a loss. Choose `n` when asked about replay.

## Invalid-input path

At the Beach, enter `banana` or `west`. The game gives an error message and retains **5 energy**. Try ` NORTH ` afterward to move to the Jungle.

## Run the automated tests

From the project folder:

```bash
python -m unittest discover -s tests -v
```

The tests check the required rules, including movement, invalid input, blocked bridge, one-time pickups, lantern requirement, winning path, energy exhaustion, replay reset, and CLI interactions.

## Project layout

```text
mystery-island/
├── main.py                # Asks for input and prints menus
├── game.py                # Game rules, functions, and player state
├── tests/
│   ├── test_game.py       # Game rule and edge-case tests
│   └── test_main.py       # User interface integration tests
├── .gitignore
├── LEARNING_GUIDE.md      # Study plan and defence questions
└── README.md
```

## Architecture

- `new_game()` creates the player state dictionary.
- `available_actions()` builds a menu based on the player's current location.
- `apply_action()` applies one game command and returns **a new state plus a message**; the original state is not mutated.
- `main.py` handles all `input()` and `print()` operations so game logic can be tested independently of the terminal.

## Known limitations

- Text-only terminal game, no save/load or graphics.
- Exactly five rooms; the world map is fixed and deterministic.
- Starting energy is tight: taking a detour or exploring can make winning impossible.
- No third-party AI API; the task is Python fundamentals, not AI integration.

## Submission evidence checklist

- [ ] Public GitHub repository/branch URL and final commit SHA
- [ ] Python version and demonstrated `python main.py` run
- [ ] `python -m unittest discover -s tests -v` output
- [ ] At least one complete win, loss, and invalid-input demonstration
- [ ] README and known limitations
- [ ] Two **personal**, honest AI learning-log entries describing experiments you ran
- [ ] Peer/mentor code audit and ability to explain every important function

> Do not mark unchecked items complete until personally verified.
