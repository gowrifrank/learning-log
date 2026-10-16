# 🧠 Quiz Log
> Every quiz question, my answer, the real answer and the lesson. ❌ questions get asked again in the **Sunday review** until I get them right.

## 📊 Scoreboard
| Date | Score | Topics |
|---|---|---|
| 2026-10-14 | 3/3 ✅ | `//` and `%`, `input()` + `int()`, `range` with step |
| 2026-10-15 | 1/3 | items vs positions, `.sort()` returns None, chaining on literals |

## 🔁 To retry on Sunday
- [ ] 2026-10-15 Q1: items vs positions with a list literal
- [ ] 2026-10-15 Q2: `x = [3, 1, 2].sort()`
- [ ] 2026-10-16 concept: does `break` exit the `if` or the loop?
- [ ] 2026-10-16 concept: does code after `return` run?
- [ ] 2026-10-16 concept: what does a function return if it never reaches `return`?

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
