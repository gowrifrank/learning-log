# 💡 Approaches & Insights
> There's always more than one way to solve a problem. This file compares the ways I found (or could have found), explains what makes each one good or bad, and names the **patterns** I'll keep reusing.
>
> 🏷 Pattern names are in **bold caps**. Learn to spot them, because they show up in almost every program.

## 🧰 Pattern library (so far)
| Pattern | Idea | Where I used it |
|---|---|---|
| **ACCUMULATOR** | Start empty (`0`, `""`, `[]`) and add on every loop round | Sum 1–100, vowel counter, Print Function, even filter |
| **FILTER** | Loop and keep only the items that pass an `if` | Even filter |
| **TWO POINTERS** | One position from the front, one from the back, moving towards each other | Palindrome method 2 |
| **BEST SO FAR** | Keep a variable holding the best value seen yet, and update it when something beats it | Second-highest (single pass) |
| **EARLY EXIT** | `break` as soon as you have the answer, so no wasted rounds | Second-highest (sorted, backwards) |
| **NEIGHBOUR COMPARE** | In sorted data, compare each item with the one next to it | Second-highest (my idea) |
| **FLATTEN WITH ELIF** | Replace nested `if` inside `else` with an `elif` chain | Python If-Else |
| **GUARD CLAUSE** | Handle bad/empty input first with an early `return` | `average([])` |
| **DRY** | Don't repeat yourself: compute once, reuse | `is_palindrome` |
| **USE A BUILT-IN** | Before writing a loop, ask "Does Python already have a tool for this?" | Palindrome `[::-1]`, `sum()`, `max()` |

## ⚖️ How to judge an approach
1. **Correct?** Does it handle the tricky inputs (duplicates, uppercase, empty, the smallest and largest values)?
2. **Readable?** Could someone else (or me in a month) understand it quickly?
3. **Efficient?** How much work does it do? Going through the list **once** beats **sorting** it, and sorting beats going through it **many times**. This only matters for big data, but it's good to start noticing.

Usually: **correct first, readable second, fast third.**

---

## 🥈 Second-highest score (Day 05 bonus / HackerRank Runner-Up)
The trap: `[95, 95, 88]` should give **88**, not 95.

### A. Sort, take position `-2` ❌
```python
scores.sort()
second = scores[-2]
```
Short, but **wrong with duplicates** of the max. My first version.

### B. Sort, walk backwards, stop where the value changes ✅ (my idea)
```python
scores.sort()
second_best = max(scores)
for i in range(len(scores) - 1, 0, -1):
    if scores[i] > scores[i - 1]:
        second_best = scores[i - 1]
        break
```
**Why it's smart:** after sorting, all copies of the max **sit next to each other** at the end. So the first place (from the back) where a value is **bigger than its left neighbour** is exactly where the max ends, and that neighbour is the answer. It uses a **property of sorted data** instead of brute force. That's **NEIGHBOUR COMPARE** + **EARLY EXIT**.

**Subtle catch I found 🔍:** with `range(len(scores) - 1, -1, -1)` the loop reaches `i = 0`, and `scores[0 - 1]` = `scores[-1]` = the **last** item. Python wraps around silently instead of crashing! It happened to be harmless here, but stopping at `0` (`range(len(scores) - 1, 0, -1)`) is safer, because `i - 1` is then always a real position.

**Cost:** sorting is the expensive part.

### C. Remove the max, then take max of the rest ✅ (FILTER)
```python
top = max(scores)
rest = []
for s in scores:
    if s != top:
        rest.append(s)
second = max(rest)
```
**Easiest to read**: it says exactly what it means. It goes through the list 3 times (`max`, the loop, `max` again), but that's still fine.

### D. One pass, track the top two ✅ (BEST SO FAR), the "pro" answer
```python
best = None
second = None
for s in scores:
    if best is None or s > best:
        second = best       # old best gets pushed down to second
        best = s
    elif s != best and (second is None or s > second):
        second = s
```
**Most efficient:** it looks at each score **once**, with no sorting. This is the classic interview answer. It's harder to get right, though: notice `second = best` must happen **before** `best = s`.

### E. Remove duplicates with `set` ✅ (coming soon)
```python
second = sorted(set(scores))[-2]
```
A `set` keeps only unique values: `set([95, 95, 88])` → `{88, 95}`. It's one line, and you'll learn it in a later lesson.

### 🏁 Verdict
| | Correct | Readable | Efficient |
|---|---|---|---|
| A. sort + `[-2]` | ❌ | ⭐⭐⭐ | ⭐⭐ |
| B. sort + backwards (mine) | ✅ | ⭐⭐ | ⭐⭐ |
| C. filter out max | ✅ | ⭐⭐⭐ | ⭐⭐ |
| D. one pass, top two | ✅ | ⭐ | ⭐⭐⭐ |
| E. `set` | ✅ | ⭐⭐⭐ | ⭐⭐ |

**For HackerRank:** any of B, C, D or E passes. **For interviews:** know D.

### ✅ My HackerRank submission (2026-10-15), approach B
```python
arr = list(map(int, input().split()))
arr.sort()
runner_up = max(arr)
for i in range(len(arr) - 1, 0, -1):   # stops at 1, so arr[i-1] never wraps around
    if arr[i-1] < arr[i]:
        runner_up = arr[i-1]
        break                            # EARLY EXIT: first step-down from the right
print(runner_up)
```
**Insight:** forgetting `break` turned "first match" into "**last** match" (`[2, 3, 5, 6, 6]` gave 2 instead of 5). **`break` is part of the logic, not an optional speed-up.**

---

## 🧩 Day 06 functions: shorter and safer versions
| Function | Mine | Better / alternative | Why |
|---|---|---|---|
| `is_even` | `if ...: return True` / `return False` | `return n % 2 == 0` | the comparison already **is** True/False |
| `is_palindrome` | `word.lower() == word[::-1].lower()` | `w = word.lower()` then `return w == w[::-1]` | lowercase once and reuse it (**DON'T REPEAT YOURSELF**) |
| `count_vowels` | ACCUMULATOR loop ✅ | `sum(1 for ch in text.lower() if ch in "aeiou")` (coming soon) | one-liner, same idea |
| `second_highest` | sort + walk back + `return` inside the loop | add `scores = sorted(scores)` + `return` **after** the loop too | no side effect on the caller's list, and it handles `[5, 5]` |
| `average` | `return sum(numbers) / len(numbers)` ✅ | `if not numbers: return 0` first | **GUARD CLAUSE**: handle empty input before it crashes |
| `grade` | early returns with `>=` ✅ | drop the `91 >=` (earlier returns already handled 90+) | each `if` can **assume** the earlier ones failed |

**New patterns:**
- **GUARD CLAUSE:** check bad or edge input at the **top** of a function and `return` early (`if not numbers: return 0`).
- **DON'T REPEAT YOURSELF (DRY):** if you write the same thing twice (`.lower()` twice), store it once.
- **NO SURPRISE SIDE EFFECTS:** a function shouldn't change the caller's data unless that's its job. Use `sorted()` (a copy) rather than `.sort()` on a parameter.

**`return` inside a loop = EARLY EXIT for functions.** It stops the loop *and* the function in one go, so `break` after it is dead code.

---

## 📅 Leap year (HackerRank: Write a function)
Rules: divisible by 4 → leap, **unless** divisible by 100 → not, **unless** divisible by 400 → leap.

### A. Mine (submitted from my phone ✅)
```python
if year % 100 == 0 and year % 400 != 0:
    return leap                    # False: centuries like 1900
elif year % 4 == 0 or year % 400 == 0:
    leap = True
return leap
```
Handles the special case **first** (a GUARD CLAUSE), smart! Small things: `or year % 400 == 0` is extra, because anything divisible by 400 is also divisible by 4. And it mixes two styles (early `return` + setting `leap`).

### B. Most specific rule first, early returns only
```python
if year % 400 == 0:
    return True
if year % 100 == 0:
    return False
return year % 4 == 0
```
Reads exactly like the rules, from the most specific to the most general.

### C. One line of boolean logic
```python
return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```
Shortest, but hardest to read. Python's own `calendar.isleap()` uses this one.

**Insight:** when rules have exceptions ("unless..."), check the **most specific exception first**. Always test the tricky years: **2000** (400 rule), **1900** and **2100** (100 rule).

---

## 🟠 LeetCode 1929: Concatenation of Array
| Version | Code | Notes |
|---|---|---|
| Mine ✅ (BUILD A LIST) | `while count < 2:` → `for i in nums: ans.append(i)` | clear; good list practice |
| Join with `+` | `return nums + nums` | one built-in operation, faster in practice |
| Repeat with `*` | `return nums * 2` | `[1, 2] * 2` → `[1, 2, 1, 2]` |

**Insights:**
- LeetCode's "Beats X%" for 0 ms vs 1 ms is **timer noise**. Resubmitting can change it. Don't chase it on tiny problems.
- All three are **O(n)**: the work grows in proportion to the list size. Real speed-ups come from doing *less work* (like Gauss's formula), not from shaving milliseconds.
- **USE A BUILT-IN** again: Python's `+`/`*` on lists run inside Python's fast core, while a loop runs step by step.

---

## 🥉 Nested Lists (HackerRank): second-lowest with names
**Mine ✅ (5 STEPS):** build `[name, score]` pairs → sorted scores → the first score bigger than the lowest (NEIGHBOUR idea, EARLY EXIT) → FILTER the names with that score → sort and print.
**Alternatives (coming soon):**
- `second = sorted(set(scores))[1]`: `set` removes duplicates, then take position 1
- a list comprehension for the FILTER: `names = sorted([n for n, s in students if s == second])`

**Insight:** the hard part wasn't the logic, it was **translating** it. Splitting into STEP comments and checking each step's data shape with `print()` turned panic into 5 small wins.

---

## 🟠 LeetCode 1480: Running Sum of 1d Array
⚓ *Port: containers loaded per hour `[3, 1, 2, 10, 1]` → running total `[3, 4, 6, 16, 17]`.*

| Version | Code idea | Notes |
|---|---|---|
| Mine ✅ | `total` + `if len(output) == 0: total = value` / `else: total += value` | works! But the `if` isn't needed: `total` starts at 0, so `0 + value` already handles round 1 |
| **Cleanest (ACCUMULATOR)** | `total = 0` → `for value in nums: total += value; output.append(total)` | no special first case, 4 lines |
| Look back | `output.append(output[-1] + value)` (after the first item) | uses `[-1]` = "last item so far" |
| **In place** | `for i in range(1, len(nums)): nums[i] += nums[i - 1]` | changes `nums` itself, so no extra list (less memory). Positions are actually needed here! |
| Built-in (coming soon) | `list(itertools.accumulate(nums))` | Python already has it |

**Insights:**
- If a special case (`if first round`) does the same thing the general case would do, **delete it**. Choosing a good starting value (`total = 0`) removes special cases.
- The in-place version is the first time **positions** are the right tool: you need `nums[i - 1]`, the item *before* this one.
- All versions are **O(n)**. The in-place one uses less extra memory.

---

## 🔁 Palindrome (Day 04)
### A. Compare with reverse ✅ (USE A BUILT-IN)
```python
word = word.lower()
is_palindrome = word == word[::-1]
```
One line, very readable. It builds a whole reversed copy, which is fine.

### B. TWO POINTERS ✅ (my idea, fixed)
```python
n = -1
count = 0
for i in range(len(inp)):
    if inp[i] != inp[n]:
        count += 1
    n -= 1
```
**Why it's a real technique:** this is how it's done in languages without `[::-1]`, and it's the basis of many interview problems.
**Improvements I could make:**
- Only check **half** the word, `range(len(inp) // 2)`, because the second half repeats the same comparisons in reverse.
- **EARLY EXIT:** `break` at the first mismatch. One mismatch already means "not a palindrome".
- Use `inp[-1 - i]` instead of a separate `n` variable.

---

## 🔤 Vowel counter (Day 04)
### A. ACCUMULATOR + `in` ✅
```python
total = 0
for ch in sentence.lower():
    if ch in "aeiou":
        total += 1
```
### B. `.count()` for each vowel ✅
```python
s = sentence.lower()
total = s.count("a") + s.count("e") + s.count("i") + s.count("o") + s.count("u")
```
Works, but goes through the sentence 5 times and repeats itself. **A is better.**

**Insight:** `ch in "aeiou"` replaces 5 `or` checks. **Membership checks (`in`)** are one of Python's superpowers.

---

## 🖨 Print Function (HackerRank)
| Approach | Code idea | Verdict |
|---|---|---|
| `end=""` | `print(i, end="")` in a loop | ✅ Simplest. No variable needed |
| String ACCUMULATOR (mine) | `result += str(i)` then print | ✅ Useful when you need the text later |
| Maths | `number = number * 10 + i` | ❌ Breaks at 10 (two digits) |
| `join` (coming soon) | `"".join(str(i) for i in range(1, n + 1))` | ✅ One line. The "Pythonic" way |

**Insight:** testing the maths idea against **n ≥ 10** caught the bug. Always test the boundary where things change (one digit → two digits).

---

## ➕ Sum of 1 to 100 (Day 03 bonus)
| Approach | Code | Work done |
|---|---|---|
| ACCUMULATOR loop | `total += i` for i in 1–100 | 100 additions |
| Built-in | `sum(range(1, 101))` | Same work, one line |
| **Maths formula** 🤯 | `n * (n + 1) // 2` | **1 calculation**, for any n! |

**The story:** young Carl Friedrich Gauss supposedly worked this out at school. Pair 1 with 100, 2 with 99, 3 with 98... and each pair makes 101. There are 50 pairs, so 50 × 101 = **5050**.
**Insight:** sometimes the best "algorithm" is **thinking** instead of looping. With n = 1 billion, the loop takes ages but the formula is instant.

---

## 🔢 Even filter (Day 03 and Day 05)
| Approach | Code | When |
|---|---|---|
| `range` with step | `range(2, 21, 2)` | ✅ When you're **generating** evens yourself |
| FILTER with `%` | `if num % 2 == 0: even.append(num)` | ✅ When the numbers **come from somewhere else** (a list or input) |
| List comprehension (coming soon) | `[n for n in numbers if n % 2 == 0]` | ✅ The one-line Pythonic FILTER |

**Insight:** if you control the data, **generate only what you need** rather than generating everything and filtering.

---

## 🌗 Python If-Else (HackerRank)
**Nested** `if` inside `else` → **FLATTEN WITH ELIF**. Use the problem's own numbers (`2 <= n <= 5`) so the code reads like the problem statement.
**Insight:** `elif` only runs when everything above it was False, so later checks can **assume** the earlier ones failed (e.g. "it's even" after handling odd).

---

## 🔁 Loops (HackerRank)
`range(0, n + 1)` gives n+1 items, but `range(n)` gives exactly n.
**Insight:** for "do something n times", **`range(n)` is the default**. Only change the start or stop when the problem says so.
