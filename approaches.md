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

## 🟠 LeetCode 1108: Defanging an IP Address
⚓ *Port: write a crane controller's address `"192.168.1.10"` safely as `"192[.]168[.]1[.]10"`.*

| Version | Code | Notes |
|---|---|---|
| Mine ✅ (string ACCUMULATOR) | loop over `ch`, add `"[.]"` or `ch` to `output` | built from scratch, great practice! |
| **Built-in (best)** | `return address.replace(".", "[.]")` | one line, the method made for this (Day 04 **USE A BUILT-IN**) |
| Split + join | `return "[.]".join(address.split("."))` | split on dots → `["192", "168", "1", "10"]` → glue back with `"[.]"` |
| List + join (pro habit) | collect pieces in a list, then `"".join(pieces)` | faster for very long strings: `+` on strings makes a brand-new string every round |

**Insights:**
- Strings **can't be changed**, so `output = output + ch` creates a *new* string each round. Fine for an IP address; for huge texts, building a list and `"".join()`-ing it once is the faster habit.
- `.split(x)` and `x.join(...)` are **opposites**: one cuts at `x`, the other glues with `x`.
- Saved to `leetcode/2026-10-20_1108_defanging_ip.py`, the first file in the solution library 📚

---

## 🟠 LeetCode 344: Reverse String (in place)
| Version | Code | Notes |
|---|---|---|
| Mine ✅ (TWO POINTERS + temp) | `swap = s[first]` → `s[first] = s[last]` → `s[last] = swap`, then move pointers | the classic swap (it's how you'd write it in C++) |
| Tuple swap | `s[first], s[last] = s[last], s[first]` | Python evaluates the right side first, so no temp variable is needed |
| Built-in | `s.reverse()` | in place, one line (like `.sort()`: changes the list, returns None) |
| Slice assignment | `s[:] = s[::-1]` | `s[:] =` replaces the *contents* of the same list |
| ❌ Trap | `s = s[::-1]` | only makes the local name `s` point to a NEW list. LeetCode's list is untouched! |

**Insights:**
- **In place** = change the existing list (the bookshelf), not build a new one. TWO POINTERS does this with O(1) extra memory.
- Two pointers only needs **half** the list: n/2 swaps.
- `s = ...` rebinds a *name*; `s[:] = ...` or `s[i] = ...` changes the *list itself*. That's the difference between a new shelf and rearranging the same shelf.

---

## 🔥 HackerRank: Lists (command processor)
| Version | Idea | Notes |
|---|---|---|
| Mine ✅ | one function per command + an `if/elif` chain on `parts[0]` | clear structure, like a real command processor |
| Shorter | call the list methods directly in the `if/elif` (`lst.append(int(parts[1]))`) | the wrappers are optional, since methods change the list in place |
| Dispatch dict (coming soon) | `{"append": lst.append, ...}`, then look up the command and call it | no long `if/elif` chain, and new commands are one line |

**Insights:**
- `.split()` gives text, so numbers need `int()` before `insert`, `remove` or `append`.
- Don't hand-write `insert`/`remove`: the built-ins already handle shifting and edge cases (USE A BUILT-IN).
- Never change a list (`.remove`) while a `for` loop walks over it, because items get skipped.

---

## 🟠 LeetCode 2149: Rearrange Array Elements by Sign (first Medium)
| Version | Idea | Notes |
|---|---|---|
| Try 1 ❌ | one loop over **all** positions `l`; even → `positives[l]`, odd → `negatives[l]` | IndexError: `l` goes 0–5, the small lists only have 0–2 |
| Fix A | same loop, but use `positives[l // 2]` / `negatives[l // 2]` | `//` turns 0,1,2,3,4,5 into 0,0,1,1,2,2 |
| Mine ✅ (Fix B) | loop over the **small** list's positions, append **two** per round | no `if/else` needed, so it's the simplest |
| Pre-sized (later) | `result = [0] * len(nums)`; positives go to slots 0,2,4… and negatives to 1,3,5… | one pass, two "write pointers" |

**Insight:** when two lists move at **different speeds** (the result grows 2 per step, each input list 1), give each its own counter, or loop over the slower one.

### Fix A in code: keep my first idea, convert the position with `//`
```python
for l in range(len(nums)):              # l = 0, 1, 2, 3, 4, 5 (big list)
    if l % 2 == 0:
        result.append(positives[l // 2])   # 0//2=0, 2//2=1, 4//2=2
    else:
        result.append(negatives[l // 2])   # 1//2=0, 3//2=1, 5//2=2
```
| `l` | even/odd | `l // 2` | appends |
|---|---|---|---|
| 0 | even | 0 | `positives[0]` = 3 |
| 1 | odd | 0 | `negatives[0]` = -2 |
| 2 | even | 1 | `positives[1]` = 1 |
| 3 | odd | 1 | `negatives[1]` = -5 |
| 4 | even | 2 | `positives[2]` = 2 |
| 5 | odd | 2 | `negatives[2]` = -4 |

Works, but needs `if/else` and a maths trick. My version (2 appends per round) says the same thing more plainly.

### Pre-sized with two write pointers: one pass, no extra lists
Instead of building `positives` and `negatives` first, **make the answer list full-size from the start** and drop each number straight into its slot:
- Positives always go to the **even** slots: 0, 2, 4…
- Negatives always go to the **odd** slots: 1, 3, 5…
```python
result = [0] * len(nums)     # [0, 0, 0, 0, 0, 0]: 6 empty slots
pos = 0                      # next free slot for a positive
neg = 1                      # next free slot for a negative
for num in nums:             # items are fine here
    if num > 0:
        result[pos] = num    # fill the slot (allowed: the slot already exists)
        pos += 2             # jump to the next even slot
    else:
        result[neg] = num
        neg += 2             # jump to the next odd slot
return result
```
| `num` | goes to | `result` after | `pos` / `neg` after |
|---|---|---|---|
| 3 | slot 0 | `[3, 0, 0, 0, 0, 0]` | 2 / 1 |
| 1 | slot 2 | `[3, 0, 1, 0, 0, 0]` | 4 / 1 |
| -2 | slot 1 | `[3, -2, 1, 0, 0, 0]` | 4 / 3 |
| -5 | slot 3 | `[3, -2, 1, -5, 0, 0]` | 4 / 5 |
| 2 | slot 4 | `[3, -2, 1, -5, 2, 0]` | 6 / 5 |
| -4 | slot 5 | `[3, -2, 1, -5, 2, -4]` | 6 / 7 |

**Why it's "better":** one loop instead of two, and no helper lists. **Why mine is fine:** at this size the difference doesn't matter, and mine is easier to read.
**New ideas here:**
- `[0] * n` makes a list with n slots, so `result[i] = ...` works (compare Day 05: `ans[0] = 5` on an empty list ❌).
- A **write pointer** is a position that jumps forward by its own rule (`+= 2`), separate from the loop. It's like TWO POINTERS from LeetCode 344, but used for *writing* instead of *swapping*.

---

## 🔥 HackerRank: Word Order (first Medium)
| Version | Code for the last part | Notes |
|---|---|---|
| Mine ✅ | `for letter, count in counts.items(): print(count, end=" ")` | works (HackerRank ignores the extra space at the end) |
| `.values()` | `for count in counts.values(): print(count, end=" ")` | only takes what's needed, no unused `letter` |
| join ⭐ | `print(" ".join(map(str, counts.values())))` | one line, no trailing space; `join` needs **strings**, so `map(str, ...)` first |
| unpack with `*` (coming soon) | `print(*counts.values())` | `*` spreads the list into separate `print` arguments, and `print` puts spaces between them |
| `Counter` (Day 13) | `from collections import Counter` · `counts = Counter(words)` | the built-in tally sheet |

**Insights:**
- A dictionary **remembers the order keys were first added**, so "order of first appearance" needs no extra work.
- Name variables after what they hold: the keys are **words**, so `for word, count in ...` (not `letter`). `i` that's never used → `_`.
- `map(int, ...)` turns text into numbers; `map(str, ...)` goes the other way (numbers → text, for `join`).

---

## 🎯 Two Sum (Day 07 bonus / LeetCode 1)
| Version | Idea | Speed | Notes |
|---|---|---|---|
| Mine ✅ (sorted input) | count the numbers `<= target`, then `j` walks back from the biggest, `i` looks for its partner in `range(j)` | two loops inside each other (slow on huge lists) | my own idea! Needs **sorted** input and numbers ≥ 0 |
| Every pair | `for j ...: for i in range(j):` with no counting step | same, two loops | works on **any** order, so it's the simplest correct version |
| TWO POINTERS (sorted) | `left = 0`, `right = len - 1`; sum too big → `right -= 1`, too small → `left += 1` | one pass | same trick as LeetCode 344 |
| `seen` dict ⭐ | for each number: `need = target - number`; if `need in seen` → `[seen[need], i]`, else `seen[number] = i` | **one pass, any order** | the LeetCode-standard answer (LOOKUP TABLE pattern) |

**Insights:**
- `i` and `j` *are* the answer (positions). `nums[i]`, `nums[j]` are only the values.
- `return` inside nested loops exits **both** loops at once, while `break` exits only the inner one.
- `range(j)` for the inner loop means a number is never paired with itself (`[3, 3]` case).
- Edge case found by testing: `0 4 5`, target 4 needs `<=`, not `<`. **Test with 0, duplicates and "no answer".**
- ⚠️ LeetCode's input is **not sorted**, and sorting it would change the positions. To submit there, use "every pair" or the `seen` dict.

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
