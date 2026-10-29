# 🧭 Revision #1: The Journey So Far (Days 01–07 + 23 problems)
> **Goal:** before Day 08, make everything from the last 2 weeks feel solid. Then a **long quiz: 10–15 questions per topic**, one topic at a time.
> Everything here comes from **my** lessons, problems and mistakes.

## 🗺 The journey in one table
| Week | Lessons | Problems | Big moments |
|---|---|---|---|
| 1 (12–18 Oct) | Days 01–06, Day 07 parts 1–2 | 9 HackerRank, 2 LeetCode | ⭐⭐ 2nd star, first LeetCode, STEP-comments method |
| 2 (19–25 Oct) | Day 07 parts 3–4 + Two Sum bonus | 3 HackerRank, 7 LeetCode | first Mediums (2149, Word Order), HackerRank Orchestrate hackathon |
| 3 (26 Oct–) | revision | LeetCode 1689, Piling Up! | ⭐⭐⭐⭐ 4th star, LeetCode Day 10 🔥 |

---

## 📋 How to revise (per topic)
1. 📖 **Read** the listed sections (read, don't copy). Tick each ✅ line in **"I can…"** only if you could do it with no notes.
2. 🐞 **Reread your own mistakes** for that topic. These are the questions most likely to come up in the quiz 😉
3. ✍️ **Rewrite from memory** the listed problem in a scratch file (`review.py`). Stuck for 5 min? Peek at **one line** only.
4. 💬 Say **"ready for topic N"** and you'll get the quiz: 10–15 questions mixing *predict the output*, *find the bug*, *write a few lines* and *explain it like a YouTube viewer*.

**Scoring:** ≥ 80% = ✅ topic done · 60–79% = retry the ❌ ones next session · < 60% = reread and redo that topic. Every quiz is logged in [quiz-log.md](../quiz-log.md).

**Suggested order (3–4 sessions, at whatever pace life allows):**
- **Session A:** Topics 1–3 (basics, conditions, loops)
- **Session B:** Topics 4–5 (strings, lists) ⭐
- **Session C:** Topics 6–8 (functions, dictionaries, parsing and printing) ⭐
- **Session D:** Topic 9 (patterns, errors, problem solving), then **Day 08** 🎉

📗 **Reference for every topic:** [python-reference.md](python-reference.md): types and their ranges, and for every built-in/method what it takes, what it gives back and when it crashes.

Warm-up drills you already have: [review-weekend-1.md](review-weekend-1.md) (strings, `map`, dicts) and [add-remove-loop-book.md](add-remove-loop-book.md) (add, remove, loop).

---

## 1️⃣ Basics: print, variables, input, types, maths (Days 01–02)
📖 **Read:** [python-reference.md](python-reference.md) §1, §6 · [notes.md](../notes.md): *Day 01*, *Day 02*, *Maths operators* · [day01.py](../day01.py), [day02.py](../day02.py)
**I can…**
- [ ] explain what a variable is and print several values with commas
- [ ] say what type `input()` gives, and convert with `int()`, `float()`, `str()`
- [ ] write an f-string with values inside `{}`, and control spaces exactly
- [ ] predict `7 / 2`, `7 // 2`, `7 % 2`, `2 ** 3`, and use `% 2 == 0` for "even"
- [ ] explain why `"12" + 3` crashes and fix it two ways
- [ ] give the range of `int`, `float`, `bool` and say what `0.1 + 0.2` and `-7 // 2` give
- [ ] say which values are falsy (and why `bool("False")` is `True`)

🐞 **My mistakes:** missing comma in `print` · f-string spacing `is{age}` · commas in `print` aren't printed
✍️ **Rewrite:** HackerRank *Arithmetic Operators* and *Python: Division*

## 2️⃣ Conditions: if / elif / else (Day 02)
📖 **Read:** [notes.md](../notes.md): *Day 02* · approaches.md: *Python If-Else*
**I can…**
- [ ] write a flat `if / elif / else` chain (no nesting) and explain why `elif` can **assume** the earlier checks failed
- [ ] use `and`, `or`, `not`, `in`, and chained ranges `2 <= n <= 5`
- [ ] pick `>` vs `>=` from the wording ("90+" means `>= 90`)
- [ ] explain why `ch == "a" or "e"` is always True and fix it

🐞 **My mistakes:** `|` used as "or" · `grade == "A"` instead of `"A"` · boundary 90 excluded
✍️ **Rewrite:** HackerRank *Python If-Else* · the Day 06 `grade()` function

## 3️⃣ Loops: for, range, while, break, continue (Day 03)
📖 **Read:** [notes.md](../notes.md): *Day 03*, *Loop keywords* · [day03.py](../day03.py)
**I can…**
- [ ] list exactly what `range(5)`, `range(1, 6)`, `range(2, 21, 2)`, `range(5, 0, -1)` give
- [ ] choose `for` (known count) vs `while` (until something changes)
- [ ] make sure every `while` loop changes something so it can end
- [ ] explain `break` vs `continue` vs `pass`
- [ ] build a total with an ACCUMULATOR (`total = 0`, `total += x`)
- [ ] write a loop that goes **backwards** over positions

🐞 **My mistakes:** `range(0, n+1)` off-by-one (HackerRank Loops) · infinite loop (344) · `range(1:n+1)` with a colon (412) · missing `break` (Runner-Up)
✍️ **Rewrite:** HackerRank *Loops* · sum 1 to 100 (three ways: loop, `sum`, Gauss)

## 4️⃣ Strings ⭐ (Day 04)
📖 **Read:** [notes.md](../notes.md): *Day 04* · [data-structures-guide.md](data-structures-guide.md) §2, §4, §6 · [add-remove-loop-book.md](add-remove-loop-book.md) §4 · review-weekend-1.md *Saturday* drills
**I can…**
- [ ] index and slice: `s[0]`, `s[-1]`, `s[1:4]`, `s[::-1]`, `s[1:]`, `s[:-1]`
- [ ] explain why strings can't be changed (`s[0] = "X"` crashes) and rebuild them with `+=`
- [ ] use `.upper()` `.lower()` `.strip()` `.replace()` `.split()` `" ".join()`, and remember they **return a new string**
- [ ] search 3 ways: `x in s` (yes/no), `s.find(x)` (position or -1), `s.count(x)` (how many)
- [ ] choose a **letters loop** vs a **positions loop**
- [ ] compare strings case-insensitively

🐞 **My mistakes:** `word[ch]` when `ch` is a letter · `.index[i]` with square brackets · `Racecar` failing without `.lower()` · `string.find(ch) == 0` (Merge the Tools)
✍️ **Rewrite:** palindrome · vowel counter · LeetCode 1108 *Defanging an IP* · HackerRank *Merge the Tools!*

## 5️⃣ Lists ⭐⭐ (Day 05)
📖 **Read:** [notes.md](../notes.md): *Day 05* · [add-remove-loop-book.md](add-remove-loop-book.md) §0–§2 (**all of it**) · [data-structures-guide.md](data-structures-guide.md) §3
**I can…**
- [ ] answer "**position or value?**" for `pop`, `insert`, `remove`, `del`, `in`, `index`
- [ ] grow a list with `.append()` (never `ans[0] = ...` on an empty list)
- [ ] say what each method **gives back** (`pop` → the item; `append`, `sort`, `remove` → `None`)
- [ ] explain `sorted(x)` vs `x.sort()`, and functions (around) vs methods (after the dot)
- [ ] loop 4 ways: items, `range(len(...))`, `enumerate`, two pointers
- [ ] read nested lists: `students[0][1]`
- [ ] explain why removing from a list while looping over it skips items

🐞 **My mistakes (9 items-vs-positions slips!):** even filter · 1929 · 1480 `output[value - 1]` · 2149 one counter for two lists · `range(list)` ×3 · `scores.max()` · `pop(blocks[0])` (Piling Up)
✍️ **Rewrite:** second-highest score (with duplicates) · LeetCode 1929, 2149 · HackerRank *Lists*, *Piling Up!*

## 6️⃣ Functions (Day 06)
📖 **Read:** [notes.md](../notes.md): *Day 06* · [lessons/day06-functions.md](day06-functions.md) · approaches.md: *Day 06 functions*
**I can…**
- [ ] write `def name(params):` with a default value, and call it
- [ ] explain `return` vs `print`, and why a function with no `return` gives `None`
- [ ] explain `break` vs `return` (loop vs whole function)
- [ ] spot a **side effect** (`scores.sort()` inside a function changes the caller's list)
- [ ] say why a variable must never share a function's name (`grade = ...`)
- [ ] write a GUARD CLAUSE for empty input

🐞 **My mistakes:** `print` instead of `return` (×3) · `return {x}` makes a set · dead code after `return` · `return` outside a function (Nested Lists, Piling Up)
✍️ **Rewrite:** `count_vowels`, `is_palindrome`, `average`, `second_highest`, `grade` as functions that **return**

## 7️⃣ Dictionaries ⭐ (Day 07)
📖 **Read:** [notes.md](../notes.md): *Day 07* · [lessons/day07-dictionaries.md](day07-dictionaries.md) · [add-remove-loop-book.md](add-remove-loop-book.md) §3 · review-weekend-1.md *Sunday* drills
**I can…**
- [ ] add, change, look up and delete: `d[k] = v`, `d[k]`, `d.get(k, 0)`, `del d[k]`, `d.pop(k)`
- [ ] say what `key in d` checks (**keys only**)
- [ ] loop over keys, values and both (`.items()`)
- [ ] write the COUNTING line from memory: `counts[x] = counts.get(x, 0) + 1`
- [ ] find the most common item with BEST SO FAR (updating **both** variables)
- [ ] explain why `d["z"] += 1` crashes on a new key

🐞 **My mistakes:** `best_count` never updated (letter counter) · counted letters instead of words (Word Order) · `counts.items` without `()`
✍️ **Rewrite:** letter counter + most common letter · Two Sum with a `seen` dict · HackerRank *Word Order*

## 8️⃣ Parsing input and printing ⭐ (HackerRank's favourite)
📖 **Read:** [data-structures-guide.md](data-structures-guide.md) §5–§6 · [add-remove-loop-book.md](add-remove-loop-book.md) §5 · [notes.md](../notes.md): *Reading many numbers from one line*
**I can…**
- [ ] read one number, a line of numbers, and "a name then numbers" (`name, *rest = input().split()`)
- [ ] explain `list(map(int, input().split()))` piece by piece, and why `map` needs `list(...)`
- [ ] read T test cases with a loop
- [ ] print on one line 3 ways: `end=" "`, `" ".join(map(str, nums))`, `print(*nums)`
- [ ] use `sep=` and f-string formatting `f"{avg:.2f}"`

🐞 **My mistakes:** `map(...).sort()` · `input.split` without `()` · used the loop's last `name` instead of `query_name` (Finding the percentage)
✍️ **Rewrite:** HackerRank *Find the Runner-Up Score!*, *Finding the percentage*, *Nested Lists*

## 9️⃣ Patterns, errors and problem solving
📖 **Read:** [approaches.md](../approaches.md): *Pattern library* + any 3 problem sections · [lessons/problem-solving-method.md](problem-solving-method.md) · [mistakes-journal.md](../mistakes-journal.md): *Focus areas* + *Daily checklist* · cheat sheet §10–§12
**I can…**
- [ ] name and write each pattern from memory: ACCUMULATOR, FILTER, COUNTING, BEST SO FAR, TWO POINTERS, EARLY EXIT, GUARD CLAUSE, FLAG, TAKE FROM BOTH ENDS, FIND THE BOTTLENECK
- [ ] look at a new problem and say which pattern fits
- [ ] use the STEP method: solve by hand → steps in English → code one step at a time
- [ ] decode errors: `SyntaxError` (missing `:`, `return` outside a function), `IndexError`, `KeyError`, `TypeError` (`str + int`, `range(list)`, `word[ch]`), `AttributeError` (`map.sort`, `scores.max`), "Time Limit Exceeded" (infinite loop)
- [ ] explain the LeetCode format (`class Solution`, **return**, inputs already typed) vs HackerRank (read `input()`, **print**)
- [ ] use the contest routine: read twice → example by hand → STEP comments → code → **Run** → Submit

✍️ **Rewrite:** LeetCode 344 (two pointers) · 1480 (accumulator) · 1689 (bottleneck) · 2161 (filter)

---

## 🏁 After the quiz
- Every ❌ goes to quiz-log.md's retry list and gets a drill in [add-remove-loop-book.md](add-remove-loop-book.md) if it's about lists, dicts or strings.
- All topics ✅ → **Day 08: sets and tuples** 🎉
- Daily minimum during revision: **1 LeetCode** (streak) and **1 commit**. The rainy-day bank in [progress.md](../progress.md) helps on busy days.
