# 🧠 Quiz Log
> Every quiz question, my answer, the real answer and the lesson. ❌ questions get asked again in the **Sunday review** until I get them right.

## 📊 Scoreboard
| Date | Score | Topics |
|---|---|---|
| 2026-10-14 | 3/3 ✅ | `//` and `%`, `input()` + `int()`, `range` with step |
| 2026-10-15 | 1/3 | items vs positions, `.sort()` returns None, chaining on literals |
| 2026-10-18 🗓 Sunday review | 7/10 | retries + data navigation, parsing, slicing |
| 2026-10-21 explain-back | 2/2 ✅ | why `int(parts[1])`, why methods change a list in place |
| 2026-10-21 thinking (Day 07 ties) | 1/1 ✅ | `>` keeps the first winner on a tie, `>=` hands it to the last |
| 2026-10-21 syntax check | 1/1 ✅ | `.items()` gives (key, value) pairs; dicts use **keys**, not index |
| 2026-10-22 syntax check | 1/1 ✅ | `list(map(int, "5 10".split()))[1]` → `10`, a number |
| 2026-10-19 quick check | ½ | positions loop: `range(nums)` → needs `range(len(nums))` |
| 2026-10-18 quick checks | 3/3 ✅ | append vs index on empty list, nested pair access, `.get()` vs `[]` on a missing key |

## 🔁 To retry on Sunday
- [ ] 2026-10-15 Q1: items vs positions with a list literal (❌ again on 10-18, retry next Sunday)
- [x] 2026-10-15 Q2: `x = [3, 1, 2].sort()` (✅ 10-18, but it's `None` in Python, not `null`)
- [ ] 2026-10-16 concept: does `break` exit the `if` or the loop? (½ on 10-18: right answer, wrong reason. `break` stops the loop completely)
- [x] 2026-10-16 concept: does code after `return` run? (✅ 10-18)
- [x] 2026-10-16 concept: what does a function return if it never reaches `return`? (✅ 10-18)
- [x] 2026-10-17 concept: trace the COUNTING pattern for "apple" (✅ 10-18)
- [ ] 2026-10-18 Q8a: what does `.split()` give? (a LIST of strings)
- [ ] 2026-10-18 Q9: `pass` + loop variable after the loop
- [ ] 2026-10-19 QC: write a loop over POSITIONS of a list (`range(len(x))`, not `range(x)`)

---

## 2026-10-14
**Q1.** `print(17 // 5, 17 % 5)`
- My answer: `3, 2` → ✅ (almost: the screen shows `3 2`)
- **Lesson:** the comma inside `print()` is code that separates items. Python prints a **space**, not a comma.

**Q2.** What's wrong? `age = input("Age? ")` then `print(age + 1)`
- My answer: wrap it in `int()` → ✅
- **Why:** `input()` always returns text. `"31" + 1` is a `TypeError`.

**Q3.** `for i in range(3, 12, 3): print(i)`
- My answer: 3, 6, 9 → ✅
- **Lesson:** the stop value (12) is never included.

---

## 2026-10-15
**Q1.** What's wrong?
```python
for i in [10, 20, 30]:
    print([10, 20, 30][i])
```
- My answer: "the list doesn't have a name, so it errors on line 1" → ❌
- **Real answer:** a list **doesn't need a name**. `[10, 20, 30]` written directly in the code (a "literal") works anywhere a list variable would. The real bug is **items vs positions, for the 5th time**: `i` is `10`, so `[10, 20, 30][10]` → `IndexError: list index out of range`.
- **Fix:** `print(i)`, because `i` already *is* the item.
- **Lesson:** values can be used **directly** without a variable: `"Robot"[0]`, `[1, 2, 3][0]` and `len("hi")` all work.

**Q2.** What gets stored in `x`? `x = [3, 1, 2].sort()`
- My answer: `[1, 2, 3]` → ❌
- **Real answer:** **`None`**! `.sort()` sorts the list *in place* and returns **nothing**. (This was in my notes from yesterday 😅)
- **Fix:** `x = sorted([3, 1, 2])` → `[1, 2, 3]`
- **Lesson:** never write `x = something.sort()`. Same trap as Day 06: a function that only `print`s gives back `None`.

**Q3.** `print("Robot"[::-1].lower())`
- My answer: "maybe `tobor`, or a compiler error" → ✅ (`tobor`), but I wasn't confident
- **Why it works:**
  1. `"Robot"[::-1]` → `"toboR"` (slicing works on a string literal, no variable needed)
  2. `"toboR".lower()` → `"tobor"`
- **Lesson: method chaining.** Python works **left to right**, and each step's result feeds into the next. `"  Hi  ".strip().upper()` → `"HI"`.

---

## 2026-10-18 🗓 Sunday review (7/10)
**Q1.** `for i in [10, 20, 30]: print([10, 20, 30][i])`
- My answer: prints 10, 20, 30 → ❌
- **Real answer:** `IndexError`. `i` is `10` (an ITEM), so `[10, 20, 30][10]` doesn't exist. **Items vs positions, 6th time.** My answer is what `print(i)` would do.

**Q2.** `x = [3, 1, 2].sort()` → I said `null` → ✅ idea, but Python calls it **`None`** (`null` is the word in other languages like Java/JavaScript).

**Q3.** `break` inside `if` inside `for` → I said "for, but the loop still continues with the next items" → ½
- **Real answer:** `break` exits the **for loop completely**. No more items are processed.
- What I described (skip to the next item) is a different keyword: **`continue`**.
```python
for n in [1, 2, 3, 4]:
    if n == 2:
        continue     # skip 2, carry on with 3
    if n == 4:
        break        # stop the whole loop
    print(n)         # prints 1, 3
```

**Q4.** Code after `return` → No ✅

**Q5.** No `return` reached → `None` ✅ (I wrote `null`)

**Q6.** Counting `"apple"` → `{'a': 1, 'p': 2, 'l': 1, 'e': 1}` ✅

**Q7.** `d["Harsh"][-1]` → `28.0` ✅, `len(d)` → `2` ✅ (counts pairs)

**Q8.** Input `4 8 15`
- (a) `input().split()`: I said `4 8 15` → ❌. It's a **list of strings**: `['4', '8', '15']`
- (b) `list(map(int, ...))` → `[4, 8, 15]` ✅
- **Lesson:** `.split()` always turns ONE string into a LIST. The quotes show they're still text.

**Q9.** `for name in [...]: pass` then `print(name)`
- My answer: Atlas, ASIMO, Optimus → ❌
- **Real answer:** just **`Optimus`**. `pass` means "do nothing" (a placeholder so the loop isn't empty), so the loop prints nothing. After it ends, `name` keeps its **last** value.

**Q10.** `"banana".count("a")` → `3` ✅, `"banana"[1:4]` → `"ana"` ✅

---

## 2026-10-18 quick checks (2/2 ✅)
**QC1.** Fix `names = []` / `names[0] = "Tina"` → `names.append("Tina")` ✅
**QC2.** `for student in [["Tina", 37.2], ["Harsh", 39.0]]`: first `student`? → `["Tina", 37.2]`, and the score is `student[1]` ✅
**QC3.** After `del robot["height"]`: `robot.get("height")` → `None` ✅, `robot["height"]` → crashes (`KeyError`) ✅

---

## 2026-10-19 quick check (½)
**QC.** In `for value in nums:` is `value` a position or an item, and how do you loop over positions? → I wrote `for value in range(nums)` → ½. `range()` needs a NUMBER: `for i in range(len(nums)):` → `i` = 0, 1, 2... and `nums[i]` = the item. (`value` itself is an **item**.)

---

## 2026-10-21 explain-back (HackerRank Lists) 2/2 ✅
**1.** Why `int(parts[1])`? → "it's a continuous string" ✅ More precisely: `.split()` always gives **text** (`"5"`), and `int()` turns it into the number `5`.
**2.** Why does `final_list.append(x)` work without `final_list = ...`? → "it affects the list directly" ✅ The method changes the list **in place** (the same object), so there's nothing to reassign.

## 2026-10-21 thinking question (Day 07 letter counter) 1/1 ✅
- **Q:** With `"noon"` (`n` and `o` both appear twice), which letter wins, and does `>` vs `>=` matter?
- **A (mine):** with `>`, `n` wins; with `>=`, `o` wins ✅
- **Why:** `n` sets the bar at 2. Then `o` has 2: `2 > 2` is False, so it can't take over; `2 >= 2` is True, so it does. A dictionary keeps the order letters were first seen, so `n` comes first.

## 2026-10-21 syntax check (`.items()`) 1/1 ✅
- **Q:** In `for letter, count in counts.items():`, what does `.items()` hand the loop each round?
- **A (mine):** the letter for `letter` and the number for `count`, the mapped pair ✅
- **Wording fix:** dictionaries have **keys**, not index positions. Each round gives one `(key, value)` pair, e.g. `('a', 3)`, unpacked into the two variables.

## 2026-10-22 syntax check (parsing one line of numbers) 1/1 ✅
- **Q:** After `nums = list(map(int, input().split()))` with input `5 10`, what is `nums[1]`? Number or text?
- **A (mine):** `10`, a number ✅ (`map(int, ...)` converted it; position 1 is the second item)

## 2026-10-27 warm-up (Add·Remove·Loop book) 2/3
- **#1** `a = [4, 3, 2]; x = a.pop(); print(x, a)` → `2 [4, 3]` ✅ (`pop()` takes the last and gives it back)
- **#2** `a = [0] * 3; a[1] = 7; print(a)` → I said `[0, 7]` ❌ → `[0, 7, 0]`. `[0] * 3` makes **three** slots `[0, 0, 0]`; `a[1] = 7` only replaces the middle one
- **#3** BEST SO FAR with `max(best, h)` over `[3, 0, 5, 1]` → `3 3 5 5` ✅

## 2026-10-28 warm-up 1.5/3
- **#1** `nums = [2, 0, 1]; print(nums[nums[0]])` → `1` ✅ (inside first: `nums[0]` = 2, then `nums[2]` = 1)
- **#2** `"banana"[1:4], "banana".count("ana")` → I said `ana 2` → ½: the slice ✅, but `count` = **1**. `count` doesn't overlap: after the "ana" at 1–3 it continues from position 4 ("na")
- **#3** `a = [5, 6, 7]; a[0] = a[2]; print(a)` → I said `7 6 7` → ½: the values ✅, but printing a list shows `[7, 6, 7]` (brackets + commas)

## 2026-10-28 Revision #1 quiz: Basics, Types, Built-ins, Operators 8.5/15 (57%) 🟡 → redo
> Rule: <60% = redo the topic. All misses fall into 4 traps (below), now with ✅/❌ examples in [lessons/python-reference.md](lessons/python-reference.md).
- **#1** `print("a", "b", 3)` → I said crash ❌ → `a b 3`. Numbers need no quotes; each comma → one space
- **#2** `f"Age is{age}!"` → `Age is30!` ✅
- **#3** `input()` type + `n * 2` → str, 55 ✅ (exactly: `'55'`, text repeated)
- **#4** `"12" + 3` → ½: I said "illegal operation" → **TypeError**; I retyped the values instead of converting: `int("12") + 3` → 15, `"12" + str(3)` → `'123'`
- **#5** `7 / 7` → 1.0, float ✅
- **#6** `bool("False"), bool(0), bool(" ")` → True False True ✅
- **#7** `int(-3.9)`, `int("12.5")` → ½: -3 ✅, but it's **ValueError** (not syntax)
- **#8** `0.1 + 0.2 == 0.3` → False ✅ (reason: binary can't store 0.1 exactly; rounding is the fix)
- **#9** int limits → ½: Python no limit ✅, C++ ≈ **2.1 billion** (I said 2.8)
- **#10** `range(10, 0, -3)`, `range(5, 0)` → ½: `[10, 7, 4, 1]` ✅, but `[]` (empty, NOT a crash)
- **#11** `x = print("hi"); print(x)` → ½: I said None → screen shows `hi` THEN `None`
- **#12** `max("Zebra", "apple")`, `sorted("cab")` → 0: `'apple'` (uppercase is smaller) · `['a', 'b', 'c']` (always a list)
- **#13** `round(2.5)`, `round(3.5)`, `sum([])`, `max([])` → 0: `2` (tie → even), `4`, `0`, ValueError
- **#14** `7 // 2`, `-7 // 2`, `7 % 2`, `2 ** 3` → ½: `-7 // 2` = **-4** (rounds toward −∞; `//` never gives decimals)
- **#15** `"ab" * 3`, `[0] * 3`, `[1] + 2` → ½: last one → TypeError
- **Traps:** (1) empty result ≠ crash · (2) TypeError vs ValueError · (3) what it gives back (`sorted` list, `print` None, `round` ties) · (4) `//` with negatives

## 2026-10-28 Revision #1 quiz RETAKE (new numbers) 13.5/15 (90%) ✅ PASSED
- **#1** `print("x", 5, "y")` → `x 5 y` ✅
- **#2** `f"Hi{name}, bye"` → `HiGowri, bye` ✅
- **#3** `type(n)`, `n + n` → str, `'44'` ✅
- **#4** `"5" + 2` → TypeError · `int("5") + 2`, `"5" + str(2)` ✅ (converted this time!)
- **#5** `9 / 3` → 3.0, float ✅
- **#6** `bool("")`, `bool("0")`, `bool([0])` → False True True ✅
- **#7** `int(7.8)`, `int("7.8")` → ½: 7 ✅, I said "InputError" → **ValueError** (InputError doesn't exist)
- **#8** why 0.1 + 0.2 ≠ 0.3 → binary storage ✅ (small fix: it's ordinary decimals like 0.1, not large numbers)
- **#9** C++ ≈ 2.1 billion, Python unlimited ✅
- **#10** `range(3, 10, 3)`, `range(8, 2)` → ½: `[3, 6, 9]` ✅, I said `0` → `[]` (an empty LIST: counting up from 8 never reaches 2)
- **#11** `ok` then `None` ✅
- **#12** `max("cat", "Dog")`, `sorted("bca")` → `'cat'`, `['a', 'b', 'c']` ✅
- **#13** → ½: `round(4.5)` 4, `round(5.5)` 6, `round(4.6)` 5 ✅ · `sum([])` → **0** (I said "can't add") · `min([])` → **ValueError**
- **#14** `9 // 2`, `-9 // 2`, `9 % 2`, `3 ** 2` → 4, -5, 1, 9 ✅ (negative floor right!)
- **#15** `hihi`, `[1, 1, 1]`, TypeError ✅
- **Still shaky:** empty cases (`range` that can't reach → `[]`, `sum([])` → 0 vs `min([])` → ValueError), and exact error names

## 2026-10-28 Revision #1 VARIETY quiz (6 formats) 8.4/10 (84%) ✅ PASSED
- **#1 Fix** `print(age + 1)` → `print(int(age) + 1)` ✅
- **#2 Fix** f-string spacing → `f"Total: {total}"` ✅
- **#3 Crash or not** → 0.4: a) `"abc"[5:]` I said IndexError → `''` (SLICES never crash) · b) `"abc"[5]` IndexError ✅ · c) `range(3, 3)` I said `[3]` → `[]` (stop is excluded, so start = stop gives nothing) · d) `max([4])` 4 ✅ · e) `int(" 8 ")` I said ValueError → `8` (spaces at the ends are OK)
- **#4 Odd one out** → `7 // 1` (int; the rest are float) ✅
- **#5 True/False** → F, T, F, F ✅ (but `-1 // 3` = **-1**, not -2: -0.33 → one step left → -1)
- **#6 Write it** last digit / remove last digit of `n = 1234` → I wrote `n.pop()` ❌ (AttributeError: an int has no `.pop()`) → `n % 10` → 4 · `n // 10` → 123
- **#7 Predict** → `12 33 43` ✅
- **#8 Match the error** → IndexError, no error, TypeError, ValueError ✅
- **#9 Blanks** `range(5, 0, -1)` ✅
- **#10 Blanks** `sep="-"` ✅
- **Still shaky:** slice `[5:]` vs index `[5]` · `range(a, a)` → `[]` · `int()` allows spaces · digit maths with `% 10` and `// 10`
