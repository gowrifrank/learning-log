# 🟩 Project: NVIDIA on my 2027 GitHub graph

## Draft design (1 Jan to 31 Dec 2027)
`#` = dark green (many commits), `.` = light green (1 commit), blank = outside 2027
```
 ....###.............................................
 ...#...#....#...#.#...#.#####.####..#####..###......
 ..#..#..#...##..#.#...#...#...#...#...#...#...#.....
 ..#.###.#...#.#.#.#...#...#...#...#...#...#####.....
 ..#..#..#...#..##..#.#....#...#...#...#...#...#.....
....#...#....#...#...#...#####.####..#####.#...#.....
.....###............................................
```
Rows = Sunday (top) to Saturday (bottom). Columns = the 53 weeks of 2027. Draft eye logo + "NVIDIA", 97 dark days.

## How the GitHub graph works
- Each square is **one day**. Its colour depends on how many contributions you made that day.
- There are **5 shades** (none, plus 4 greens). The shades are **relative to your own busiest days**, not fixed numbers.
- 2027 starts on a **Friday**, so the first column only has Fri and Sat.

## The plan: keep the daily streak AND draw the art
Blank squares would break my streak, so instead:
| Pixel | Commits that day | Shade |
|---|---|---|
| `.` background | **1–2** (my normal daily commit) | lightest green |
| `#` art | **10+** (make sure to stay consistent) | darkest green |

On "dark" days, I do my lesson as many small, real commits (one per exercise part, notes, journal, HackerRank solution files...).

## Rules
- ✅ Every commit is **real work** on that day. No fake or back-dated commits.
- ✅ Commit email = my GitHub account email, or the commits won't count.
- ✅ Commit to the **default branch** (`main`). Commits on other branches don't count until they're merged.
- ⚠️ Never skip a day. A missing day makes a white hole in the drawing.
- ⚠️ Keep every other day **low** (1–2 commits). A random 15-commit day would add an extra dark pixel.

## 🛠 To build (December 2026): `art_planner.py`
A real Python project that I write myself:
1. Store the design as a list of strings (lists = Day 05!).
2. Loop over every date of 2027 with the `datetime` module.
3. Work out each date's row (weekday) and column (week).
4. Print a calendar: `2027-01-05 → DARK (10+ commits)`.
5. Bonus: print **today's target** every time I run it.

## ⏳ Status
- [x] Draft design (2026-10-14)
- [ ] Polish the logo (try a closer NVIDIA "eye" shape)
- [ ] Write `art_planner.py` (December, once I know lists, functions and modules)
- [ ] Start on 1 Jan 2027 🚀
