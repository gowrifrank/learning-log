# 🐞 My Mistakes Journal
> Every mistake I've made, why it happened and how I fixed it. Read the **Focus areas** and **Daily checklist** every day before coding.

## 🎯 Focus areas (my patterns so far)
0. ⭐ **Navigating data: strings, `map`, dictionaries, searching, parsing and printing.** My biggest weak spot (confirmed 2026-10-23). Read [lessons/data-structures-guide.md](lessons/data-structures-guide.md) before every problem until it feels natural.
1. **Letters vs positions in loops.** I keep mixing up `for ch in word` (gives letters) and `for i in range(len(word))` (gives positions). This has happened **9 times** (palindrome, vowel counter, even filter, quiz Q1 twice, LeetCode 1929, LeetCode 1480, Piling Up `pop(value)`...)! Drill it with [lessons/add-remove-loop-book.md](lessons/add-remove-loop-book.md) §0.
2. **Off-by-one with `range`.** `range` stops **before** the stop value. Count the items for a small input before submitting.
3. **`=` replaces, `+=` adds on.** When building a total or a string across a loop, I need `+=`.
4. **Text vs numbers.** `input()` gives text, `int()` converts to a number, and `str()` converts back. I can't mix them with `+`.
5. **Case-sensitivity.** `"R" != "r"`. Use `.lower()` before comparing or checking letters.
6. **Not testing tricky inputs.** Test duplicates, uppercase, empty input, and check the output uses my new variable.
7. **`print` instead of `return` in functions.** Functions should return the answer, and the caller prints it.
8. **Jumping straight to code.** When I'm confused, I should solve it by hand first, then write the steps in English, then translate to Python.

## 🛠 Syntax I'm still building (practise these!)
| Skill | Status | Correct form |
|---|---|---|
| Grow a list | 🟢 quick check ✅ 10-18 | `x = []` then `x.append(item)`, never `x[0] = item` on an empty list |
| Items vs positions | 🔴 9 slips | `for item in x:` → use `item`. `for i in range(len(x)):` → use `x[i]` |
| Function vs method | 🟡 | `sorted(x)`, `len(x)`, `max(x)` (around) · `x.sort()`, `x.append()` (after the dot) |
| `=` vs `==` | 🟡 | `=` stores, `==` compares |
| `return` vs `print` | 🟡 | `return` only inside `def`. HackerRank main code → `print` |
| Nested data `[name, score]` | 🟢 got it 10-18 (Nested Lists + quick check ✅) | `pair[0]` = name, `pair[1]` = score |
| Parsing input | 🟡 | `list(map(int, input().split()))` |
| `map` both ways | 🔴 | `map(int, texts)` → numbers · `map(str, nums)` → texts (for `join`) · always wrap in `list(...)` to look inside |
| Searching a string | 🔴 | `x in s` (yes/no) · `s.find(x)` (first position, `-1` if missing) · `s.count(x)` (how many) |
| Dict lookups | 🟡 | `d[key]` (crashes if missing) · `d.get(key, 0)` (safe) · `key in d` checks **keys** only |
| Dict loops | 🟡 | `for k in d:` keys · `for v in d.values():` values · `for k, v in d.items():` both |
| Printing on one line | 🟡 | `print(x, end=" ")` · `" ".join(map(str, nums))` · `print(a, b, sep=", ")` |
| Position tools vs value tools | 🔴 new 10-26 | `x.pop(i)` `x.insert(i, v)` `del x[i]` take a **position** · `x.remove(v)` `v in x` take a **value** · `x.pop()` = last, `x.pop(0)` = first |
| `range(number)` not `range(list)` | 🔴 4 slips (10-19, 10-24, 10-26, 10-27) | `range(len(nums))` or `range(n)` |
| One answer per test case (FLAG) | 🟡 new 10-26 | `ok = True` → on failure `ok = False; break` → after the loop `print("Yes" if ok else "No")` |
| Crash or not? | 🟡 variety quiz 10-28: `"abc"[5:]` (slice → `''`), `range(3, 3)` (→ `[]`), `int(" 8 ")` (→ 8) | empty results are answers, not crashes: `[]`, `''`, `-1`, `None`, `0` · numbers in `print` need no quotes |
| Name the error | 🟡 retake 10-28: TypeError ✅, but "InputError" for `int("7.8")` | wrong **type** (`"12" + 3`, `[1] + 2`) → `TypeError` · right type, bad **content** (`int("12.5")`, `max([])`) → `ValueError` |
| What does it give back? | 🟢 retake 10-28 (`sorted`, `print`, `round`, `//` all ✅) | `sorted("cab")` → `['a', 'b', 'c']` (list!) · `print()` → `None` (but still prints) · `round(2.5)` → `2` (ties → even) · `-7 // 2` → `-4` |
| Digit maths | 🔴 new 10-28 | `n % 10` = last digit (1234 → 4) · `n // 10` = drop the last digit (1234 → 123) · ints have no `.pop()` |
| Naming | 🟡 | name variables after what they hold *right now* (`lowest`, not `second_low`) |

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
- [ ] Want the **first** match in a loop? Did I add `break`?
- [ ] Does every `while` loop change something that will eventually make its condition False?
- [ ] Does my function **return** (not print)? Did I test the **boundary values** (e.g. exactly 90)?

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

### 2026-10-15: HackerRank, Find the Runner-Up Score! ❌ → ✅ Submitted!
**Problem 1:** `AttributeError: 'map' object has no attribute 'sort'`
```python
arr = map(int, input().split())
arr.sort()                       # ❌ arr is a "map", not a list
```
**Why:** `map(int, ...)` doesn't build a list. It's a "recipe" that makes the numbers one at a time when asked, and a recipe has no `.sort()`.
**Fix:** wrap it in `list()`: `arr = list(map(int, input().split()))`, or use `sorted(arr)`, which accepts anything loopable and returns a list.

**Problem 2:** forgot `break` in the backwards loop.
```python
for i in range(len(arr) - 1, 0, -1):
    if arr[i-1] < arr[i]:
        runner_up = arr[i-1]     # keeps overwriting all the way down!
```
**Why:** without `break`, the loop carries on to the start of the list, and every later "step down" overwrites the answer. `[2, 3, 6, 6, 5]` → sorted `[2, 3, 5, 6, 6]` → it ends with **2**, not 5.
**Fix:** add `break` straight after `runner_up = arr[i-1]` (EARLY EXIT).
**Lesson:** when I want the **first** match, I need `break`. Otherwise I get the **last** match. Trace a tricky input by hand before submitting.

**What went right ✅:** used `range(len(arr) - 1, 0, -1)` (stops at 1, so no wrap-around with `arr[-1]`). That was applied straight from approaches.md!

### 2026-10-15: Day 06, Functions (VS Code) 🟡
**Problem 1: `print` instead of `return`** in `count_vowels`, `second_highest` and `average`.
They *show* the answer but give back `None`, so `x = average(scores)` would store `None`. The functions can't be reused in other code.
**Fix:** `return total` / `return second_best` / `return sum(numbers) / len(numbers)`, and do the printing **outside**, where the function is called.
**Lesson:** a function should **calculate and return**. The caller decides what to do with the answer (print it, compare it, store it).

**Problem 2: forgot "ignore case".** `is_palindrome("Racecar")` → False, and `count_vowels("OPTIMUS")` → 0. (Case-sensitivity again! Focus area #5.)
**Fix:** `word = word.lower()` at the start of the function.

**Problem 3: `second_highest` changed the caller's list.** `scores.sort()` inside the function also sorts the list that was passed in, which is a surprise **side effect**.
**Fix:** `scores = sorted(scores)` makes a sorted *copy* and leaves the original alone.

**Problem 4: bonus `grade()` returned False.**
```python
return grade == "A"     # ❌ == COMPARES ("is grade equal to A?" → False)
```
**Why:** `==` asks a question and gives True/False. `=` stores a value. Here I didn't need either: just `return "A"`.
**Also:** `score > 90` excludes 90 itself (the task said 90+, so `>= 90`), and `91 > score > 75` excludes 75. With early returns, upper limits aren't needed, because the earlier `return` already handled the higher scores.
**Lesson:** check the **boundary values** (90, 75, 50) exactly. "90+" means `>= 90`.

### 2026-10-16: Day 06, fix round 2 (VS Code) ✅ mostly
**Fixed:** all functions now `return`, `grade` boundaries use `>=`, `average` returns `79.0`.
**Bugs found while fixing:**
- **`break` got deleted** during editing, so `second_highest` returned 61 instead of 88 (last step-down instead of first). Lesson: after editing, **re-run the tricky tests**.
- **`{sum(numbers)/len(numbers)}`** left over from an f-string: `return {x}` returns a **set** `{79.0}`, not a number. Curly braces only mean "insert value" **inside f-strings**.
- **`break` after `return`** never runs, because `return` already ended the function (dead code).
- **No `return` after the loop:** `second_highest([5, 5])` → `None`, because the loop never hits `return` and the function "falls off the end". Fix: put `return second_best` **after** the loop as well.
- **Edge case:** `average([])` → `ZeroDivisionError`. Think about empty input.

### 2026-10-17: HackerRank, Finding the percentage ❌ → ✅
**Problem:** printed Anurag's average (28.00) instead of Harsh's (26.50).
```python
for _ in range(n):
    name, *line = input().split()
    ...
avg = sum(student_marks[name]) / len(student_marks[name])   # ❌ `name` = LAST student read
print(f"{avg:.2f}")
query_name = input()                                        # ❌ read AFTER using it
```
**Why:**
1. After a loop ends, the loop variable keeps its **last** value. `name` was "Anurag", not the student we were asked about.
2. The average was calculated **before** `query_name` was even read. Order of lines matters.
3. Test case 0 passed by **luck**, because the asked student happened to be the last one.

**Fix:** put the average **after** `query_name = input()` and look up `student_marks[query_name]`.
**Also:** the floats were already converted on line 6 (`list(map(float, line))`), so no second conversion was needed.
**Lesson:** use the variable that holds **what the question asks for**. When one test passes and another fails, ask "what's different about the failing input?"

### 2026-10-18: LeetCode 1929, Concatenation of Array ❌ → ✅ Accepted 92/92
```python
n = len(list)            # ❌ `list` is Python's TYPE name, not my data → "object of type 'type' has no len()"
...
for i in nums:           # ❌ i = ITEMS again (7th time!), but used as positions in ans[i]
    ans[i] == nums[i]    # ❌ == compares, it doesn't store (same as grade() on Day 06). And `ans` was never created
...
print(ans)               # ❌ LeetCode needs `return`, not print
```
**Lessons:**
- Use the **parameter's name** (`nums`), never the type (`list`). Same for `str`, `dict`, `int`: never name your own variables these either.
- An empty list `[]` has no positions to fill, so `ans[0] = 5` → IndexError. **Grow a list with `.append()`**.
- `=` stores, `==` compares.
- LeetCode/functions: **return** the answer.
- `+` on two lists **joins** them: `[1, 2] + [1, 2]` → `[1, 2, 1, 2]`.
**2nd try bug:** `ans.append(nums[i])` with `for i in nums` gave `[2, 1, 2, 2, 1, 2]` for `[1, 2, 1]`. `i` was the item (1, 2, 1), so `nums[i]` fetched position 1, 2, 1 → 2, 1, 2. **Fix:** `ans.append(i)`, since `i` already IS the number. Tracing it in a table made the bug obvious.

### 2026-10-18: HackerRank, Nested Lists 😰 → ✅
**Problem:** I had the right logic but froze writing the code: an uncreated list filled by index, `list.sorted()`, comparing positions instead of values, `return` outside a function.
**What fixed it:** the **STEP-comments method** ([lessons/problem-solving-method.md](lessons/problem-solving-method.md)). I split it into 5 steps, coded one at a time, and checked each with `print()`. Steps 3–5 I wrote **myself** ✅
**Small improvement:** `second_low = scores[0]` holds the **lowest** at first, so the name is misleading. Better: `lowest = scores[0]`, then `second = score` inside the loop.

### 2026-10-19: LeetCode 1480, Running Sum ❌ → ✅ Accepted 54/54
```python
for value in nums:
    ...
    output.append(output[value - 1] + value)   # ❌ value is an ITEM, used as a POSITION
```
**Why:** with `nums = [1, 2, 3, 4]`, round 2 has `value = 2`, so `output[1]`, but `output` only has 1 item (`[1]`) → IndexError. **Items vs positions, 8th time.**
**What I meant:** "the **last** running total so far" = `output[-1]` (negative index from Day 04!).
**Even simpler:** keep a `total` ACCUMULATOR and append it. Then there's no need to look back into the list or treat the first item specially.

### 2026-10-21: LeetCode 344, Reverse String ❌❌ → ✅
**Try 1: "Time Limit Exceeded"**
```python
while (first < last):
    ...swap...           # ❌ first and last never change → infinite loop
```
**Why:** the loop condition can never become False. The code didn't crash, it just never finished. Same trap as forgetting `count -= 1` (Day 03).
**Fix:** move the pointers inside the loop: `first += 1`, `last -= 1`.

**Try 2: wrong answer, the list came back unchanged ("double swapping" 😄)**
```python
for letter in s:         # ❌ repeats the WHOLE reversal once per letter
    first = 0
    last = len(s) - 1
    while first < last: ...
```
**Why:** "Hannah" has 6 letters → reversed 6 times → an even number of reversals = back to the start. (`letter` was never used, which was a hint it wasn't needed.)
**Fix:** delete the outer `for` loop.
**Lessons:**
- Every `while` loop needs something inside it that moves it towards stopping.
- If a loop variable is never used, ask "do I need this loop at all?"

### 2026-10-21: HackerRank, Lists (first draft review)
- `input.split()` ❌ is missing the `()`. `input` is the function itself, `input()` *calls* it → `AttributeError`
- `Final_List = ""` ❌ is an empty **string**. An empty list is `[]`
- `parts[1]`, `parts[2]` are **text**. Wrap them in `int()` before inserting, appending or removing numbers
- Hand-written `insert` / `remove` loops: the `while` loops never change `i` (infinite) and run past the end of the list. **Python already has `.insert(i, x)` and `.remove(x)`** (USE A BUILT-IN)
- Changing a list (`.remove`) while looping over it with `for` skips items. Avoid it
- Style: `snake_case` for variables (`final_list`). `CapitalWords` is reserved for classes

### 2026-10-21: Day 07, Letter counter (BEST SO FAR) 🟡
```python
for letter, count in counts.items():
    if count > best_count:
        best_letter = letter      # ❌ best_count is never updated → stays 0
```
**Why:** every count is `> 0`, so every letter "wins" and the **last** one is left over ("banana" → `n`).
**Fix:** a BEST SO FAR update changes **both** variables: the winner *and* the score to beat.
**Lesson:** if a variable is used in a comparison but never changes inside the loop, the comparison never gets harder.

### 2026-10-21: Day 07, Grade book 🟡 output ✅, reuse ❌
- Output was correct, but the `if/elif` grading logic was **re-typed inside the loop** instead of calling the Day 06 `grade()` function. The task was to *reuse* it (DRY: write it once, call it many times).
- A variable named `grade` would **overwrite** a function named `grade`. Never give a variable the same name as a function.
- `91 >= score` in the B branch is never needed: a score of 90 or more already returned/stopped at the A branch.

### 2026-10-22: Day 07 bonus, Two Sum (own sorted idea) 🟡 → ✅
- `range(1, count, -1)` ❌ gave **nothing**: going *down* from 1 never reaches `count`. Backwards = `range(count - 1, -1, -1)` (start high, step -1)
- A variable (`highest`) set to the **same value every round** never moves. Use the loop's own position (`nums[j]`) instead
- Inner loop named `value` but it held **positions** → renamed `i` (items vs positions, again)
- `break` exits only the inner loop → put the loops in a function and `return [i, j]`
- `nums[i] < target` missed `0 + 4 = 4`. Fix: `<=`. **Found by testing an edge case (0)**
- Leftover variables (`highest`, `lowest`, `seen`) that nothing reads: delete them

### 2026-10-22: LeetCode 2149, Rearrange by Sign (first Medium) ❌ → ✅
```python
for l in range(len(nums)):          # l = 0..5 (big list)
    if l % 2 == 0:
        result.append(positives[l])  # ❌ positives only has 0..2 → IndexError at l = 3
```
**Why:** one counter was used for **two lists of different sizes**. The big list moves 2 steps for every 1 step in each small list (and items got skipped too).
**Fix:** loop over the small list (`range(len(positives))`) and append two items per round (or use `l // 2`).
**Lesson:** "index out of range" → ask **"which list is this position for, and how long is that list?"**

### 2026-10-22: HackerRank, Word Order (first Medium) ❌ → ✅
- `for wd in word:` ❌ looped over the **letters** of each word, so it counted letters. `word` is already one whole word → tally it directly. (*"What am I holding?"* a word, not a list of words)
- `print(counts.items)` ❌ is missing `()` (same trap as `input.split`), and the task wanted `len(counts)`
- `.items()` gives `(word, count)` pairs; `.values()` gives just the counts
- `print(x, " ")` prints each on a new line → `print(x, end=" ")` keeps them on one line

### 2026-10-23: LeetCode 2161, Partition by Pivot ❌ → ✅
- `pivot = []` ❌ **overwrote the parameter** `pivot` (the number 10) with an empty list. One name holds one thing → named the list `equals`. (Same trap as `grade = None` vs `def grade`)
- `if nums < pivot:` ❌ compared the **whole list**, not one number → `nums[i]`. A non-empty list counts as "bigger" than `[]`, so every number went into `more` and the output equalled the input.
- **Debug clue:** "output = input, unchanged" usually means every item took the **same branch**.

### 2026-10-23: HackerRank, Merge the Tools! (own logic, no hints) ❌ → walkthrough → ✅
- `factor = len(string) / k` is the **number of pieces**, but it was used as the **piece length**. It only worked because both were 3. Piece length = `k`
- `string.find(ch) == 0` ❌ asks "does this letter first appear at position 0 of the **whole** string?" The real question: "have I already kept it **in this piece**?" → `if ch not in result:`
- One shared `output` list sliced with **string** positions → wrong sizes (same lesson as 2149). Fix: a fresh `result = ""` per piece
- `print(list)` shows `['A', 'B']`. Build a **string** to print `AB`
- 💡 The window idea (`pos`, `mul`) was right! `range(0, len(string), k)` does that jumping for you

### 2026-10-24: LeetCode 1672, Richest Customer Wealth ❌ → ✅
- `if balance > winner` ❌ missing `:` → SyntaxError (every `if`/`for`/`while`/`def` line ends with `:`)
- `range(temp_acc)` ❌ `range` needs a **number**, not a list → `range(len(temp_acc))` (2nd time: also on 19 Oct)
- ✅ Reset `balance = 0` per customer in the right place (yesterday's "reset per group" lesson stuck!)

### 2026-10-25: LeetCode 412, Fizz Buzz ❌ → ✅
- `range(1:n+1)` ❌ → `range(1, n+1)`: `range` takes **commas**, slicing takes colons
- `elif elif` ❌: a word typed twice → SyntaxError
- `result.append(i)` ❌ → `str(i)`: the answer is `list[str]`
- ✅ Nice idea: exclusive conditions (`and i % 5 != 0`) make the order of checks irrelevant

### 2026-10-26: LeetCode 1689, Deci-Binary Partitions ✅ (logic first, on paper)
- 💡 **My greedy idea** (subtract the biggest deci-binary number that fits, repeat) gives the right answer, but listing all deci-binary numbers doubles per digit (2, 4, 8, 16...), and `n` can have 100,000 digits → impossible.
- **The insight came from tracing my own greedy column by column:** each number takes at most 1 from every column, so the **biggest digit** decides the answer. Code = BEST SO FAR over the characters (5 lines).
- **Lesson:** when a hand-method works, **trace it on paper and look for what decides the count**. The "pattern" often collapses into one simple rule.

### 2026-10-26: HackerRank, Piling Up! (own idea) ❌❌ → walkthrough → ✅ ⭐⭐⭐⭐
- `return "No"` / `return "Yes"` ❌ **outside a function** → SyntaxError. HackerRank main code **prints**
- `range(blocks)` ❌ → `range(len(blocks))` (3rd time `range(list)`)
- `blocks.pop(blocks[0])` ❌ **pop wants a POSITION**: with a first cube of 4 it removes `blocks[4]`. → `blocks.pop(0)` (first), `blocks.pop()` (last). Then `blocks.pop(1)` ❌ = the **second** cube, not the last
- `topblock` was saved but **never compared** → the rule ("a cube must not be bigger than the one below") was never checked. Two names for two ideas: `picked` (in my hand) vs `top` (on the pile)
- `print("No")` inside the loop + `print("Yes")` always after it → printed **both**. Fix: an `ok` **flag**, `break` on failure, one print after the loop
- `elif ... and blocks[0]:` compared nothing (a number on its own is just "truthy") → plain `else:`
- 💡 **Right from the start:** pop from the ends and always take the bigger end
- **Lesson:** before coding, write the **rule** as an `if` in English ("if picked > top → fail"). If that `if` isn't in my code, the rule isn't being checked.

### 2026-10-27: LeetCode 42, Trapping Rain Water (first Hard) 😵 → picture → blanks → ✅
- Hand table gave **negative water** (-3, +1, -1...) ❌. Water can never be negative → the walls were wrong. Walls = the **tallest bar anywhere** on each side, **including the bar itself**, not the neighbours
- What made it click: a **picture** (bars + water + the shorter-wall line) → [lessons/img/rain_water.png](lessons/img/rain_water.png)
- `[0] * 3` then `a[1] = 7` → I said `[0, 7]` ❌ → `[0, 7, 0]`: replacing keeps the length
- `[0] * 5` ❌ hard-coded the example's length → `[0] * n` (LeetCode tests every size)
- `range(height)` ❌ → `range(n)` (**4th** `range(list)`!)
- Backwards loop started at `0` ❌ → `range(n - 1, -1, -1)`: the last position is `n - 1`
- `min(left_max, right_max) - height` ❌ whole lists → `min(left_max[i], right_max[i]) - height[i]`. Inside a positions loop, **every list needs its `[i]`** (same slip as 2161 `nums < pivot`)
- **Lesson:** when the words don't make sense, **draw it**. And for a Hard, one step at a time (print each row) beats writing it all at once.

### 2026-10-28: LeetCode 1920 ✅ first try · HackerRank Find a String 🟡 → ✅
- 1920: `range(len(nums))` right first time 🎉 (after 4 `range(list)` slips). `nums[nums[i]]` read inside-out
- Warm-up: `"banana".count("ana")` → **1**, not 2: `count` never overlaps · `print(list)` shows `[7, 6, 7]` with brackets
- Find a String: `if flag == "True":` ❌. `.find()` returns a **position** or **-1**, never True/False, and `"True"` in quotes is text anyway → `if pos != -1:`
- `flag = False` straight before `flag = string.find(...)` was dead code (overwritten at once)
- 💡 Own idea that worked: `find(sub, i, end)` with `end += 1` = a sliding window
- **Lesson:** before using a method, ask **"what does it give back?"** (see [lessons/python-reference.md](lessons/python-reference.md))

### 2026-10-28: Revision #1 quiz (Basics, Types, Built-ins, Operators) 8.5/15 🟡
- **What went wrong:** I guessed "crash" for things that just give an empty result (`range(5, 0)` → `[]`), thought numbers in `print` need quotes, used vague error names ("illegal operation", "invalid syntax"), and wasn't sure what `sorted`, `print`, `round` and `max([])` give back.
- **Why:** I'd only read the reference once, and its "notes / crashes" column was too short to learn from.
- **Fix:** the reference now has ✅/❌ examples for every tool, a "do NOT crash" list and a "which error is it?" guide. Retry the ❌ questions next session.
- **Remember:** `-7 // 2` → `-4` (down = toward −∞) · uppercase < lowercase (`'Z'` 90, `'a'` 97) · fix `"12" + 3` by **converting** (`int()` / `str()`), not by retyping
- **Retake (same day, new numbers): 13.5/15 = 90% ✅.** `//` with negatives, `round` ties, `sorted`, `print` all fixed. Still shaky: empty cases (`range(8, 2)` → `[]`, `sum([])` → `0`, `min([])` → ValueError) and the name ValueError ("InputError" isn't a Python error).
- **Variety quiz (6 formats): 8.4/10 = 84% ✅.** Misses: slice `[5:]` vs index `[5]` (only the index crashes), `range(3, 3)` → `[]`, `int(" 8 ")` → 8, and `n.pop()` on an int → use `n % 10` / `n // 10`.

### 2026-10-29: LeetCode 1281, Subtract Product and Sum of Digits ❌❌ → ✅
- `list{n}` ❌ **SyntaxError**: curly braces → function calls always use **round** brackets `list(n)`
- `list(n)` would still crash: `n` is an **int**, and an int can't be looped over (`TypeError: 'int' object is not iterable`)
- `list("n")` ❌ **ValueError** `int('n')`: quotes = the **letter** n, not the variable → `str(n)` (the variable turned into text)
- ✅ `int(number)` on each character: `for` over a string gives **text** characters like `'2'`
- 💭 I thought strings can't be looped over like lists. They can (since Day 04: `for ch in word`)
- **Lesson:** read the last line of the error: `int() with base 10: 'n'` shows exactly what `int()` received

### 2026-10-30: LeetCode 1342, Steps to Reduce a Number to Zero 🟡 → ✅
- Run passed 3/3 ✅, but `num = 0` would have returned **1** ❌ (loop skipped, then the final `steps += 1` still ran). The constraint says `0 <= num`, so 0 is a hidden test → added `if num == 0: return steps` (GUARD CLAUSE)
- `num = num / 2` ❌ turns 14 into `7.0` (a float) → `num // 2` keeps it an int
- 💡 Own shortcut that works: `while num > 1` + one extra step for 1 → 0
- **Lesson:** "Accepted" on **Run** only checks the examples. Before **Submit**, trace the **smallest allowed input** from the constraints (same family as the quiz's empty cases)
