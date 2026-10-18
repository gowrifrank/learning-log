# 📒 My Python Cheat Sheet

## Day 01: print and variables
```python
print("Hello")             # shows text on screen
name = "Gowri"             # variable = a labelled box that stores a value
print("My name is", name)  # commas add a space between items
```

## Day 02: input, int, f-strings, if/else
```python
name = input("Name? ")       # input() ALWAYS gives text (a string)
age = int(input("Age? "))    # int() turns text "31" into number 31
print(f"Hi {name}, next year you'll be {age + 1}")  # f-string: {} gets replaced by its value

if age >= 30:                # the 4-space indent = "this belongs to the if"
    print("30 or older")
elif age >= 18:              # elif = "else if": only checked when the ones above were False
    print("18 to 29")
else:
    print("under 18")
```
- `0 < x < 10` checks a range in one go (`and` works too)

## Maths operators (HackerRank)
| Operator | Example | Result | Meaning |
|---|---|---|---|
| `+` `-` `*` | `7 * 2` | `14` | add, subtract, multiply |
| `/` | `7 / 2` | `3.5` | float division, always gives a decimal (`8 / 2` → `4.0`) |
| `//` | `7 // 2` | `3` | integer division, drops the decimal part |
| `%` | `7 % 2` | `1` | remainder, `n % 2 == 0` means n is **even** |
| `**` | `3 ** 2` | `9` | power, 3 squared |

## Day 03: Loops
```python
for i in range(5):           # repeats 5 times, i = 0, 1, 2, 3, 4
    print(i)

for letter in "Gowri":       # loops over each letter of a string
    print(letter)

count = 5
while count > 0:             # repeats WHILE the condition is True
    print(count)
    count -= 1               # same as count = count - 1 (forget it = infinite loop!)

total = 0
for i in range(1, 101):      # building a total: start at 0, add each round
    total += i
print(total)                 # 5050
```
| Code | Gives |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 (starts at 0, stops **before** 5) |
| `range(1, 6)` | 1, 2, 3, 4, 5 (start, stop-before) |
| `range(2, 21, 2)` | 2, 4, … 20 (start, stop, step) |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 (counting down) |

- **`for`** = you know how many times. **`while`** = repeat until something changes.
- Stuck in an infinite loop? Press **Ctrl+C** in the terminal.
- ⚠️ **Off-by-one error**: `range(0, n+1)` gives n+1 items, not n. Use `range(n)` for exactly n items.
- `+=` `-=` `*=` are shortcuts: `x += 1` means `x = x + 1`.
- Use clear variable names (`total`, not reusing `count`) and keep comments matching the code.

## Day 04: Strings
```python
robot = "Optimus"
len(robot)        # 7, number of characters
robot[0]          # "O", first letter (index starts at 0)
robot[-1]         # "s", negative index counts from the end
robot[0:3]        # "Opt", slice [start:stop], stops BEFORE stop (like range)
robot[3:]         # "imus", missing stop = until the end
robot[::-1]       # "sumitpO", step -1 = reversed
```
```
 O  p  t  i  m  u  s
 0  1  2  3  4  5  6
-7 -6 -5 -4 -3 -2 -1
```
**String methods**: they return a NEW string and never change the original (save it: `name = name.strip()`)
| Method | Example → result |
|---|---|
| `.upper()` / `.lower()` | `"Hi".upper()` → `"HI"` |
| `.strip()` | `"  hi  ".strip()` → `"hi"` (removes spaces at both ends) |
| `.replace(old, new)` | `"Sankar".replace("a", "@")` → `"S@nk@r"` |
| `.count(x)` | `"Sankar".count("a")` → `2` |
| `x in text` | `"ank" in "Sankar"` → `True` |

**Comparing strings**
- `==` / `!=` work on strings, **case-sensitive**: `"Racecar" == "racecaR"` → `False`
- Fix: `.lower()` both sides before comparing
- Palindrome: `word.lower() == word.lower()[::-1]`

**Looping: letters vs positions**
| Loop | Gives you | Use it as |
|---|---|---|
| `for ch in word:` | letters | `ch` |
| `for i in range(len(word)):` | positions | `word[i]` |

**Joining strings**
```python
"ab" + "cd"          # "abcd", + joins text
str(5)               # "5", number → text (the opposite of int())
"12" + 3             # ❌ TypeError: convert first with str(3)
result = ""          # build text in a loop, like total = 0
for i in range(1, 4):
    result += str(i) # "1" → "12" → "123"
```

**print tricks**
```python
print("A", "B", sep="-")   # A-B   (sep = what goes between items, default is a space)
print("Hi", end="")        # no newline at the end
```
- The commas inside `print(a, b)` are code, not output. Only what's inside quotes gets printed.

**⚠️ Traps I fell into**
- `|` is NOT "or". Use the word `or`.
- `ch == "a" or "e"` is ❌ always True. Write `ch in "aeiou"` instead.
- `word[ch]` when `ch` is already a letter crashes: "string indices must be integers"
- `.index` is a method, so call it with `( )` not `[ ]`

## Day 05: Lists
```python
robots = ["Optimus", "Atlas", "ASIMO"]   # many values in one variable
robots[0]          # "Optimus", indexing and slicing work like strings
robots[-1]         # "ASIMO"
len(robots)        # 3
```
**Changing a list** (lists CAN be changed, strings can't)
| Code | Does |
|---|---|
| `robots.append("Spot")` | add to the end |
| `robots.insert(0, "Figure")` | add at a position |
| `robots.remove("Atlas")` | remove by **value** |
| `robots.pop(1)` | remove by **position** (and give it back). `pop()` = last item |
| `robots[1] = "Gen 3"` | replace an item |

**Functions vs methods**
| Functions go AROUND | Methods go AFTER the dot |
|---|---|
| `len(x)` `sum(x)` `max(x)` `min(x)` `sorted(x)` | `x.sort()` `x.append()` `x.remove()` `x.pop()` |
- ❌ `scores.max()` crashes. ✅ `max(scores)`
- Average = `sum(scores) / len(scores)`

**`sorted()` vs `.sort()`**
| | `sorted(scores)` | `scores.sort()` |
|---|---|---|
| Original | unchanged | changed |
| Gives back | new sorted list | `None`! (never write `x = scores.sort()`) |
- Largest first: `sorted(scores, reverse=True)`

**Looping**
```python
for robot in robots:               # ITEMS: use robot directly
for i in range(len(robots)):       # POSITIONS: use robots[i]
for score in scores[::-1]:         # backwards (or reversed(scores))
for i in range(len(x) - 1, -1, -1):  # positions backwards: 4, 3, 2, 1, 0
```
- 🔑 Name the loop variable after what it IS: `num`, `robot` = item. `i` = position.
- `break` stops the loop immediately.

**Building a list**
```python
even = []                 # start empty
for num in numbers:
    if num % 2 == 0:
        even.append(num)
```
**Joining and repeating lists**
```python
[1, 2] + [3, 4]    # [1, 2, 3, 4]
[1, 2] * 2         # [1, 2, 1, 2]
ans = []
ans[0] = 5         # ❌ IndexError: an empty list has no slot 0
ans.append(5)      # ✅ append creates a new slot
```
- `x[i] = ...` only REPLACES an existing slot. To GROW a list, use `.append()`.
- Never name a variable `list`, `str`, `dict` or `int` (those are Python's type names).

**Strings ↔ lists**
```python
"I love robots".split()        # ['I', 'love', 'robots']
" ".join(["I", "love", "robots"])  # "I love robots"
```

**Reading many numbers from one line (HackerRank)**
```python
arr = list(map(int, input().split()))
# "2 3 6 6 5" → split() → ["2","3","6","6","5"] → map(int, ...) → list → [2, 3, 6, 6, 5]
```
- `map(func, items)` applies `func` to every item, but gives a lazy "recipe", **not a list**.
- ❌ `map(...).sort()` crashes. Wrap it: `list(map(...))`

**Literals and chaining**
- Values work directly without a variable: `[10, 20, 30][0]` → 10, `"Robot"[0]` → "R"
- Methods chain **left to right**: `"Robot"[::-1].lower()` → `"toboR"` → `"tobor"`

**Second-highest with duplicates** (`[95, 95, 88]` → 88): skip every value equal to `max`, or sort and walk backwards until the value changes.

## Day 06: Functions
```python
def square(n):            # def name(parameters):
    return n * n          # return hands the value back

result = square(5)        # 25
def power(base, exp=2):   # default value
    return base ** exp
```
**`break` vs `return`**
| | `break` | `return` |
|---|---|---|
| Exits | the nearest **loop** (`for`/`while`), NOT the `if` | the **whole function** (loops included) |
| Code after it | rest of the function still runs | **nothing** after it runs |
- Inside a function, `return` inside a loop does the job of `break` + return, so you don't need both.
- A function that never reaches `return` gives back **`None`** ("falls off the end").
- `print` inside a function only SHOWS. Use `return` so the caller can use the value.
- `{x}` means "insert value" ONLY inside f-strings. `return {x}` returns a set!
- Variables made inside a function stay inside.

## Loop keywords: `break`, `continue`, `pass`
| Keyword | Does |
|---|---|
| `break` | stops the **whole loop** right now |
| `continue` | skips the **rest of this round**, then goes to the next item |
| `pass` | does **nothing** (a placeholder so a block isn't empty) |
- `None` is Python's word for "nothing" (other languages say `null`)

## Day 07: Dictionaries (in progress)
> ⭐ Weak spot: see the full guide **[lessons/data-structures-guide.md](lessons/data-structures-guide.md)** (containers, nested data, looping, parsing input, printing).

```python
robot = {"name": "Optimus", "year": 2022}   # key: value pairs
robot["name"]              # "Optimus", look up by KEY
robot.get("price", 0)      # 0 if missing (no KeyError crash)
robot["price"] = 20000     # add or change
del robot["year"]          # delete
for key, value in robot.items():   # loop over both
```
**COUNTING pattern = a tally sheet ✏️**
```python
counts = {}
for ch in "banana":
    counts[ch] = counts.get(ch, 0) + 1   # "current number (or 0) + 1"
# {'b': 1, 'a': 3, 'n': 2}
```
- Long form: `if ch in counts: counts[ch] += 1` / `else: counts[ch] = 1`
- `counts[ch] += 1` on a missing key → **KeyError**. That's why we need `if` or `.get(ch, 0)`.

## 🔥 HackerRank solved
- Python If-Else
- Arithmetic Operators
- Python: Division
- Loops
- Print Function ⭐⭐
- Find the Runner-Up Score!
- Write a function (leap year)
- Finding the percentage
- Nested Lists
