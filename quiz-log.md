# 🧠 Quiz Log
> Every quiz question, my answer, the real answer and the lesson. ❌ questions get asked again in the **Sunday review** until I get them right.

## 📊 Scoreboard
| Date | Score | Topics |
|---|---|---|
| 2026-10-14 | 3/3 ✅ | `//` and `%`, `input()` + `int()`, `range` with step |
| 2026-10-15 | 1/3 | items vs positions, `.sort()` returns None, chaining on literals |
| 2026-10-18 🗓 Sunday review | 7/10 | retries + data navigation, parsing, slicing |
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
