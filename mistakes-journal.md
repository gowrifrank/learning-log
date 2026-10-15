# 🐞 My Mistakes Journal
> Every mistake I've made, why it happened and how I fixed it. Read the **Focus areas** and **Daily checklist** every day before coding.

## 🎯 Focus areas (my patterns so far)
1. **Letters vs positions in loops.** I keep mixing up `for ch in word` (gives letters) and `for i in range(len(word))` (gives positions). This has happened **4 times** (palindrome, vowel counter, even filter...)!
2. **Off-by-one with `range`.** `range` stops **before** the stop value. Count the items for a small input before submitting.
3. **`=` replaces, `+=` adds on.** When building a total or a string across a loop, I need `+=`.
4. **Text vs numbers.** `input()` gives text, `int()` converts to a number, and `str()` converts back. I can't mix them with `+`.
5. **Case-sensitivity.** `"R" != "r"`. Use `.lower()` before comparing or checking letters.
6. **Not testing tricky inputs.** Test duplicates, uppercase, empty input, and check the output uses my new variable.
7. **Jumping straight to code.** When I'm confused, I should solve it by hand first, then write the steps in English, then translate to Python.

## ✅ Daily checklist (before I click Run or Submit)
- [ ] Did I solve a small example **by hand** first?
- [ ] For a loop: am I getting **letters or positions**? Do I need `range(len(...))`?
- [ ] Does my `range` give exactly the right numbers? (Check the first and last values.)
- [ ] Am I **replacing** (`=`) or **adding on** (`+=`)?
- [ ] Am I mixing **text and numbers**? Do I need `int()` or `str()`?
- [ ] Could uppercase input break it? Should I use `.lower()`?
- [ ] Do my prompts end with `": "` and do my f-strings have the right spaces?
- [ ] Do my comments match what the code actually does?
- [ ] Did I test a **tricky** input (duplicates, uppercase, edge values)?
- [ ] Function or method? `max(x)` goes around, `x.sort()` goes after the dot

---

## 📅 Log

### 2026-10-13: Day 01 (VS Code)
**Problem:** Program crashed with a `SyntaxError`.
```python
print("My current age is", age "Next year I will be ", age+1)   # ❌
```
**Why:** missing comma after `age`. Each item in `print( )` must be separated by a comma.
**Fix:** `print("My current age is", age, "Next year I will be", age + 1)`
**Lesson:** read the line the error points to and check commas and brackets first.

### 2026-10-13: Day 02 (VS Code)
**Problems:**
- Asked for the robot's name (`choice`) but never used it. I also forgot one of the exercise steps (printing the robot's age).
- `print(f"{robot} is{robot_age} years old.")` printed `Optimus is2 years old.`

**Why:** inside an f-string, spaces are printed exactly as typed.
**Fix:** `f"{robot} is {robot_age} years old."` and re-read the exercise steps before saying "done".
**Lesson:** run the program and **read the output word by word**.

### 2026-10-13: HackerRank, Python If-Else ✅
**Problem:** none, it passed! But the code was nested (`else:` containing another `if`).
**Better:** a flat `if / elif / elif / else` chain that uses the same numbers as the problem (`2 <= n <= 5`).
**Lesson:** `elif` only runs if everything above was False, so it doesn't need nesting.

### 2026-10-13: HackerRank, Loops ❌ → ✅
**Problem:** "Wrong Answer". My output looked right, but the output box was **scrolled**, and there was a hidden 6th line (`25`).
```python
for i in range(0, n+1):   # ❌ gives n+1 numbers
```
**Why:** off-by-one. For n = 5, `range(0, 6)` is 0–5, which is 6 numbers.
**Fix:** `range(n)` gives exactly n numbers, 0 to n-1.
**Lesson:** count the expected lines and **scroll the output box**.

### 2026-10-13: Day 03 (VS Code)
**Problems:**
- `range(2, 22)` for "2 to 20": it works, but it's confusing. `range(2, 21)` is clearer.
- `if(i % 2 == 00):` doesn't need brackets, and `00` is just `0`.
- Reused `count` for the countdown **and** the sum. Use a clear name like `total`.
- The comment said "0 to 100" but the code did 1 to 100.

**Lesson:** clear names and correct comments matter as much as working code.

### 2026-10-14: Quiz, commas in `print`
**Confusion:** I thought `print(17 // 5, 17 % 5)` shows a comma.
**Answer:** the comma is **code** (it separates items), and Python prints a **space**: `3 2`.
**Lesson:** only text inside quotes (or `sep=`) appears on screen.

### 2026-10-14: Day 04, Palindrome (VS Code) ❌ → ✅
**Problem:** `TypeError: 'builtin_function_or_method' object is not subscriptable`
```python
for i in inp:                       # ❌ i is a LETTER, not a position
    if i.index[i] == i.index[n]:    # ❌ .index is a method, called with ( ) not [ ]
```
**Why:** mixed up letters and positions, and used a method I didn't understand.
**Fix 1 (simple):** `if inp == inp[::-1]:` (I already had `[::-1]` in Part 2!)
**Fix 2 (my idea, fixed):** `for i in range(len(inp)):` and compare `inp[i]` with `inp[n]`, with `n -= 1` every round.
**Also learned:** strings can be compared with `==`, but it's **case-sensitive**, so `Racecar` failed until I used `.lower()`.
**Lesson:** before writing a loop, ask "Do I already have a tool that does this?"

### 2026-10-14: Day 04, Vowel counter (VS Code) ❌ → ✅
**Problem:** `TypeError: string indices must be integers, not 'str'`
```python
for ch in ip_word:
    if ip_word[ch] == 'a'| 'e'| 'i'| 'o'| 'u':   # ❌❌
```
**Why:**
1. `ch` is already the letter, so `ip_word[ch]` is wrong (letters vs positions **again**).
2. `|` is not "or" in Python. And `ch == 'a' or 'e'` is also wrong, because it's always True.

**Fix:** `if ch in "aeiou":` and loop over `ip_word.lower()` so `OPTIMUS` works.
**Lesson:** use `in` to check "is it one of these?"

### 2026-10-14: HackerRank, Print Function ❌ → ✅
**Problem:** got lost mixing 3 ideas at once (string joining, `end=""`, maths).
```python
for i in range(1, n+1):
    str_number = i*mul    # ❌ multiplies AND replaces the value every round
```
**Why:** `=` overwrites, so only the last value survives. And I needed to **join** text, not multiply.
**Fix:**
```python
str_number = ""
for i in range(1, n + 1):
    str_number += str(i)    # str() turns a number into text, += joins it on
print(str_number)
```
**Other ways:** `print(i, end="")` inside the loop (shortest). The maths way, `number = number * 10 + i`, **breaks at n ≥ 10** because 10 has two digits.
**Lesson:** when confused, **slow down**: solve by hand, then write the steps in English, then write the code. One idea at a time.

### 2026-10-14: Day 05, Even filter (VS Code) ❌ → ✅
**Problem:** `IndexError: list index out of range`
```python
numbers = [3, 8, 15, 22, 7, 4]
for i in numbers:              # i = 3, 8, 15... these are ITEMS, not positions
    if numbers[i] % 2 == 0:    # ❌ numbers[8] doesn't exist (only 6 items)
        even.append(numbers[i])
```
**Why:** letters/items vs positions, **for the 4th time**. `for x in list` already gives the item itself.
**Fix:**
```python
for num in numbers:
    if num % 2 == 0:
        even.append(num)
```
**Lesson:** name the loop variable after what it **is**. `num` and `robot` mean items, `i` means a position. If I write `for i in numbers`, the name `i` tricks me into thinking it's a position.

### 2026-10-14: Day 05, Second-highest score (VS Code) 🟡 logic ✅, output ❌
**Problem 1:** wrote `scores.max()`, which crashes with `AttributeError`.
**Why:** `max()` is a **function** that goes *around* the list: `max(scores)`. Methods like `.sort()` and `.append()` go *after* it.
| Functions (around) | Methods (after the dot) |
|---|---|
| `len(x)` `sum(x)` `max(x)` `min(x)` `sorted(x)` | `x.sort()` `x.append()` `x.remove()` `x.pop()` |

**Problem 2:** the backwards loop correctly found `second_best`, but the `print` still showed the OLD formula `scores[len(scores)-2]`, so the new variable was **never used**.
**Fix:** `print(f"The Second-Highest score is: {second_best}")`
**Lesson:** after writing new logic, check that the output actually **uses** it. Test with the tricky input (`[95, 95, 88, 61]` → 88), not just the easy one, because both versions give 88 for the easy list.

**What I figured out myself 💡:** after sorting, walk backwards and stop at the first spot where `scores[i] > scores[i-1]`. That skips all duplicates of the max. Tested: `[95, 95, 88, 61]` → 88 ✅, `[61, 95, 95, 95]` → 61 ✅.
