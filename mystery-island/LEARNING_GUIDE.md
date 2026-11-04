# Beginner Engineering Learning Guide

This project is a reference implementation generated with AI assistance, **not proof of independent mastery**. Your assignment explicitly asks you to understand and defend each design choice. Build your own version after studying this one.

## Five short study missions

1. **Input and strings:** Find the player's name in `main.py`. Explain `input`, `.strip()`, and f-strings. Change the welcome message yourself.
2. **Variables and conditions:** Trace `energy`, `location`, and `inventory` after `north`, `take rope`, and `east`. Explain how `if` chooses a branch.
3. **Loops:** Find both `while` loops in `main.py`. Predict precisely what stops each loop. Add a friendly help message.
4. **Functions and dictionaries:** Open `game.py`. Explain why `ROUTES` is a dictionary and why `apply_action` does not call `input()`.
5. **Testing and debugging:** Run tests; deliberately change a rule to make one test fail, then repair it. Write a new test for a repeated lantern pickup.

## Rigorous engineering defence questions

1. Why does the code use a **list** for `inventory` instead of a string?
2. What is the difference between `print()` and `return` in this project?
3. Explain the difference between `choice.strip().lower()` and `choice.strip().lower`.
4. Why does invalid input leave energy unchanged?
5. What happens when energy is 1 and the player makes a legal move?
6. Why is `max(0, energy - 1)` used? Could a different design satisfy the rules?
7. Where does the project stop a player from crossing the bridge without rope?
8. Why is the beacon action separate from arriving at the Lighthouse?
9. How does `main.py` prevent the menu from continuing after a win or a loss?
10. Why is `new_game()` called again when replaying? What could go wrong with reusing inventory?
11. What does `deepcopy` prevent in `apply_action()`?
12. Show a test that fails if invalid commands reduce energy.
13. Why does the winning path have only 1 energy left?
14. How do you prove an item cannot be picked up twice?
15. Which design decision would you change in your own version, and how would you test it?

## Personal AI learning log — fill in yourself

**Entry 1**
- Concept:
- What AI explained:
- Code I personally wrote or changed:
- Command I ran and actual result:
- What I concluded:

**Entry 2**
- Concept:
- What AI explained:
- Code I personally wrote or changed:
- Command I ran and actual result:
- What I concluded:

## Reflection paragraph — write in your own words

> The concept I understand now that I didn't before is ...

Do not invent independent testing or claim this AI-generated version was entirely your own. Ask a peer to review the code, then practise defending it without assistance.
