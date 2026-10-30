# Task 2 (Medium): Dungeon Escape

**File name:** `dungeon.py`

---

## The story

You are trapped in a dungeon. Find the exit before the guards catch you!
The game is played in the terminal. The map is made of letters and symbols.

```
##########
#P..T...E#
#.##.##D.#
#K...G...#
##########
```

---

## The symbols

| Symbol | What it is | What happens |
|---|---|---|
| `P` | **you** (the player) | you start with **3 health** |
| `E` | the **exit** | step on it = you **WIN** |
| `#` | wall | you can't walk through it |
| `.` | floor | you can walk here |
| `T` | trap | stepping on it = **−1 health**. The trap stays (it hurts every time) |
| `+` | potion | **+1 health**, but health can never go above 3. The potion disappears |
| `K` | key | you pick it up (Keys +1). The key disappears from the map |
| `D` | locked door | you can only go through if you have a key. The key is used up and the door becomes floor `.` |
| `G` | guard | chases you (see below) |

The **edge of the map** works like a wall.

---

## Moving

| Key | Direction |
|---|---|
| `W` | up |
| `A` | left |
| `S` | down |
| `D` | right |

Upper and lower case both work (`w` = `W`).

**If you can't move there** (wall, edge, locked door without a key, or a guard is standing
there), **nothing happens**: no move is counted and the guards don't move.

---

## One turn, step by step

When you make a move that is allowed:

1. You move one square. **Moves +1.**
2. The square you landed on does its thing (trap, potion, key, exit...).
   - Landed on `E` → **WON**. The game ends immediately (guards don't move).
   - Health 0 or less → **LOST**. The game ends immediately.
3. **Then every guard moves one step** (see the guard rules).

---

## Guard rules (read carefully: this is the important part)

After each of your moves, each guard takes **one step toward you**:

1. If the guard is **not in your column**, it first tries to step **left or right** toward you.
2. If that is not possible (or it is already in your column), it tries to step **up or down** toward you.
3. If neither step is possible, it **stays where it is**.

Guards **cannot** walk onto: walls `#`, locked doors `D`, the exit `E`, the edge of the map,
or a square where another guard is standing. (A door you opened has become floor `.`, so guards can use it.)
Guards **can** walk over traps `T`, keys `K` and potions `+`. Nothing happens to them, and the item stays.

**Order:** guards move one by one, in **reading order**: top row first, and from left to right
inside a row (like reading a book). Use where they are **before** they move.

### Being caught
If a guard's step would land **on you**:
- you lose **2 health**,
- the guard **goes back to the square where it started the game** (if another guard is
  standing there, it just stays where it is),
- you don't move.

### Guard example
We count rows and columns from **0** (top row = row 0, left column = column 0):

```
row 0  #######
row 1  #P....#     P = row 1, column 1
row 2  #....G#     G = row 2, column 5
row 3  #E....#
row 4  #######
```
You press `S`. You move down to row 2, column 1. Now the guard moves: it is **not** in your
column (5 ≠ 1), so it steps **left** toward you, to row 2, column 4:
```
#######
#.....#
#P..G.#
#E....#
#######
```

---

## Undo

`U` undoes your last move **completely**: your position, health, keys, the items on the map
**and the guards**. Everything goes back exactly as it was before that move.
- You can undo up to **5 moves** in a row. More than that → nothing happens.
- Moves that didn't happen (blocked by a wall) are **not** saved, so undo skips them.
- Nothing to undo → nothing happens.

> Tip: the easiest way to do undo is to save a full **copy** of the game state before each move.
> Search "python copy.deepcopy".

---

## Score

- Status `WON`: **Score = 100 − moves + 20 × health left** (never below 0)
- Otherwise: **Score = 0**

Example: won in 6 moves with 2 health → 100 − 6 + 40 = **134**.

---

## How to run it: two ways

### 1) Play mode (for humans)
```
python dungeon.py map.txt
```
Show the board and the status, then wait for a command:

| Command | Does |
|---|---|
| `W` `A` `S` `D` | move |
| `U` | undo |
| `SAVE name` | save the game to the file `name.json` |
| `LOAD name` | load the game from the file `name.json` |
| `Q` | quit |

You may show friendly messages like "You can't go there."

### 2) Replay mode (for testing: your mentor's tests use this!)
```
python dungeon.py map.txt --moves DDSAU
```
- Plays the moves in the text one by one (`W`,`A`,`S`,`D`,`U`, upper or lower case).
- After the game is WON or LOST, the remaining letters are ignored.
- Then prints the **final board and status, and nothing else**, in exactly this format:

```
<the board, with P and G where they are now>
Health: <number>
Keys: <number>
Moves: <number>
Status: <PLAYING or WON or LOST>
Score: <number>
```

Extra options:
- `--save file.json` → after the moves, save the game to that file
- `python dungeon.py --load file.json --moves DD` → load a saved game (no map file), then play the moves

After loading, the game must continue **exactly** as if it had never stopped, and **undo must
still work**.

> Use `argparse` for the command line. Search "python argparse tutorial".

---

## Checking the map (do this first)

Check in this order. Print the message and exit with code 1:

| Problem | Print |
|---|---|
| The file is empty | `ERROR: map is empty` |
| Not all rows are the same length | `ERROR: rows have different lengths` |
| A symbol not in the table above (e.g. `X`) | `ERROR: unknown symbol 'X'` (the first one you find, reading top to bottom, left to right) |
| Not exactly one `P` | `ERROR: map needs exactly one P` |
| No `E` | `ERROR: map needs at least one E` |
| The map file doesn't exist | `ERROR: file not found: <file name>` |
| A letter in `--moves` that isn't W A S D U | `ERROR: unknown move 'X'` (shown in upper case) |

---

## Examples

This folder contains **`map_easy.txt`** and **`map_sample.txt`**.

### Example 1: walk to the exit
`map_easy.txt`:
```
#########
#P..T..E#
#########
```
`python dungeon.py map_easy.txt --moves DDDDDD` prints:
```
#########
#...T..P#
#########
Health: 2
Keys: 0
Moves: 6
Status: WON
Score: 134
```
Why: 6 steps right. On the 3rd step you hit the trap (3 → 2 health). The 6th step lands on the exit.
Score = 100 − 6 + 20 × 2 = 134.

### Example 2: the guard chases you
`python dungeon.py map_sample.txt --moves S` prints:
```
##########
#...T...E#
#P##.##D.#
#K..G....#
##########
Health: 3
Keys: 0
Moves: 1
Status: PLAYING
Score: 0
```
You moved down. The guard was in another column, so it moved one step **left** toward you.

### Example 3: pick up the key
`--moves SS` → you step on `K` (Keys: 1), and the guard moves left again:
```
##########
#...T...E#
#.##.##D.#
#P.G.....#
##########
Health: 3
Keys: 1
Moves: 2
Status: PLAYING
Score: 0
```

### Example 4: undo
`--moves SSU` → the board is exactly the same as Example 2 again (the key is back on the map,
Keys: 0, the guard is back too).

### Example 5: caught!
`--moves SSD` → you move right. The guard's step left lands **on you**: −2 health, and the guard
goes back to where it started:
```
##########
#...T...E#
#.##.##D.#
#.P..G...#
##########
Health: 1
Keys: 1
Moves: 3
Status: PLAYING
Score: 0
```

---

## Python you will use
- **Classes**: e.g. `Game`, `Player`, `Guard` (try `@dataclass`)
- **Lists of lists** for the map (`grid[row][col]`)
- **`copy.deepcopy`** for undo
- **`json`** for save/load
- **`argparse`** for `--moves`, `--save`, `--load`
- **Exceptions** for bad maps (e.g. your own `class MapError(Exception)`)

## Step-by-step guide (suggested)
1. Read the map file into a list of lists. Find `P` and the guards. Print the board.
2. Check the map (the error table).
3. Moving the player + walls + the edge of the map.
4. Traps, potions, keys, doors, exit, health, WON/LOST, score.
5. Replay mode `--moves` with the exact output format. Compare with the examples above.
6. Guards (rules + order + being caught). Test with Examples 2–5.
7. Undo.
8. Save/load (`--save`, `--load`, and `SAVE`/`LOAD` in play mode).
9. Play mode loop.
10. Your tests in `tests/test_dungeon.py` (at least 12). Make small maps in your tests!

## Checklist before you submit
- [ ] All 5 examples above give exactly the same output
- [ ] Every map error from the table works and nothing crashes
- [ ] Undo brings back guards, items and health
- [ ] Save → load → the game continues the same (and undo still works)
- [ ] At least 12 tests, all passing
- [ ] Committed and pushed
