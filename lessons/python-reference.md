# 📗 Python Reference: Types, Ranges & Built-ins
> Every tool I've used so far, with **real examples**: what it takes, what it gives back, ✅ how to use it and ❌ how NOT to.
> **How to read the examples:** the code is on the left. After the `#` is what Python gives back (or prints). `✅` = the right way, `❌` = a trap or a crash (with the exact error).
> Golden question before using any tool: **"What does it give back?"** (a value, a new copy, or `None`?)
> Every example here was run in Python 3.12 to check it.

### 🎯 My quiz traps (Revision quiz, 28 Oct): read these first
| Trap | Example | Where |
|---|---|---|
| An empty result is **not** a crash | `list(range(5, 0))` → `[]` · `"x".find("q")` → `-1` · `"banana"[10:]` → `''` | §7 crash or not |
| Name the error | wrong **type** → `TypeError` (`"12" + 3`) · right type, bad **content** → `ValueError` (`int("12.5")`) | §7 |
| What does it give back? | `sorted("cab")` → a **list** `['a', 'b', 'c']` · `print()` → `None` · `round(2.5)` → `2` | §2 |
| `//` rounds **down** (toward −∞) | `-7 // 2` → `-4`, not `-3` and never `-3.5` | §6 |
| Uppercase is *smaller* | `max("Zebra", "apple")` → `'apple'` (Z = 90, a = 97) | §2 max |

---

## 1. 🧱 Data types and their ranges
| Type | What it holds | Range / size | Example | Changeable? |
|---|---|---|---|---|
| `int` | whole numbers | **no limit** in Python (it grows as needed) | `42`, `-7` | no |
| `float` | decimal numbers | about **±1.8 × 10³⁰⁸**, accurate to ~**15 digits** | `3.5`, `7 / 2` | no |
| `bool` | yes/no | only `True` or `False` (they act like `1` and `0`) | `True + True` → `2` | no |
| `str` | text | any length; positions `0 … len-1` (or `-len … -1`) | `"Hi"` | **no** (build a new one) |
| `NoneType` | "nothing" | only `None` | a function with no `return` gives `None` | no |
| `list` | ordered items | any length, any mix of types | `[3, "a", 2.5]` | **yes** |
| `dict` | key → value pairs | any size; keys must be unchangeable (`str`, `int`, `tuple`) | `{"a": 1}` | **yes** |
| `tuple` *(Day 08)* | ordered items, frozen | like a list you can't change | `(1, 2)` | no |
| `set` *(Day 08)* | unique items, no order | duplicates vanish | `{1, 2}` | yes |

### `int` has no limit (C++ does)
```python
2 ** 100        # 1267650600228229401496703205376   Python just grows the number
2 ** 31 - 1     # 2147483647   = the biggest int in C++ (about 2.1 billion)
```
In C++ (later!), going past 2,147,483,647 breaks the number, so LeetCode constraints matter more there.

### `float` is approximate
```python
0.1 + 0.2                    # 0.30000000000000004   tiny error!
0.1 + 0.2 == 0.3             # ❌ False
round(0.1 + 0.2, 2) == 0.3   # ✅ True: round first, then compare
float("1e309")               # inf   too big for a float
float("inf") > 10 ** 100     # True  "bigger than any number" (Piling Up!)
```
**Why the error?** Computers store decimals in binary (0s and 1s). 0.1 can't be stored exactly in binary, just like 1/3 can't be written exactly in decimal (0.3333…). Rounding is the **fix**, the binary storage is the **reason**.

### Truthy and falsy (what `if x:` thinks)
```python
bool(0), bool(0.0), bool(""), bool([]), bool({}), bool(None)   # all False: "empty / zero / nothing"
bool(5), bool(-1), bool([0])       # True   any non-zero number, any non-empty list
bool(" ")                          # True   ← a space IS a character, so not empty
bool("0")                          # True   ← non-empty text
bool("False")                      # True   ← the WORD False is still non-empty text
if nums:                           # ✅ short for "if the list is not empty"
```

### Positions: what's allowed
```python
s = "banana"     # length 6 → positions 0…5, or -6…-1
s[0], s[-1]      # 'b' 'a'
s[5]             # 'a'   the last one = len - 1
s[6]             # ❌ IndexError: string index out of range
s[2:100]         # ✅ 'nana'   slices NEVER crash, they just stop at the end
s[10:]           # ✅ ''       empty, no crash
```

---

### 🔄 Converting between types

#### `int(x)`: make a whole number
**Takes:** text of a *whole* number, a float, or a bool · **Gives back:** `int`
```python
int("42")            # ✅ 42
int(" -7 ")          # ✅ -7     spaces and a sign are OK
int("8 9")           # ❌ ValueError   a space in the MIDDLE is not OK
int("")              # ❌ ValueError   empty text
int(12.9)            # ✅ 12     cuts off the decimals (NO rounding!)
int(-2.5)            # ✅ -2     cuts toward 0
int(True)            # 1
int("12.5")          # ❌ ValueError: invalid literal for int() with base 10: '12.5'
int(float("12.5"))   # ✅ 12     text → float → int
int("abc")           # ❌ ValueError
```
**The quotes are NOT the problem.** `int()` is *made* to read text. It first trims spaces off both ends, and then the text must be only digits (with an optional `-` or `+` in front). A dot, a letter, a middle space or empty text → `ValueError`.

#### `float(x)`: make a decimal number
```python
float("3.5")     # ✅ 3.5
float(7)         # ✅ 7.0
float("inf")     # ✅ inf
float("abc")     # ❌ ValueError: could not convert string to float: 'abc'
```

#### `str(x)`: make text (never crashes)
```python
str(5)               # ✅ '5'
"Age: " + str(30)    # ✅ 'Age: 30'
"Age: " + 30         # ❌ TypeError: can only concatenate str (not "int") to str
```

#### Fixing `"12" + 3` two ways (quiz Q4)
```python
"12" + 3          # ❌ TypeError: text + number can't mix
int("12") + 3     # ✅ 15      make BOTH numbers → it adds
"12" + str(3)     # ✅ '123'   make BOTH text → it joins
```
Don't fix it by retyping the values (`12 + 3`). In real code the `"12"` comes from `input()` or `.split()`, so you have to **convert** it.

#### `list(x)`: make a list from anything loopable
```python
list("abc")                  # ✅ ['a', 'b', 'c']
list(range(3))               # ✅ [0, 1, 2]
list(map(int, ["1", "2"]))   # ✅ [1, 2]
list({"a": 1, "b": 2})       # ['a', 'b']   keys only
list(5)                      # ❌ TypeError: 'int' object is not iterable
```

#### `type(x)`: what am I holding?
```python
type(3)        # <class 'int'>
type(3.0)      # <class 'float'>
type(7 / 7)    # <class 'float'>   / always gives a float
type("3")      # <class 'str'>
```

---

## 2. 🧰 Built-in functions (they go AROUND: `len(x)`)

#### `print(...)`: show on screen
**Takes:** any values · **Gives back:** **`None`** (it only *shows*)
```python
print("a", "b", 3)                  # a b 3   numbers need no quotes; each comma → one space
print("a", "b", sep="-")            # a-b     sep = what goes between
print("a", end=" "); print("b")     # a b     end = what goes after (default: new line)
age = 30
print(f"Age is {age}!")             # ✅ Age is 30!
print(f"Age is{age}!")              # ❌ Age is30!   spaces are exactly what you type
x = print("hi")                     # the screen shows: hi
print(x)                            # the screen shows: None   ← print gave back nothing
```

#### `input()`: read one line
**Gives back:** **always text**, even if you type a number
```python
n = input()                              # you type 5
n                                        # '5'    TEXT
n * 2                                    # ❌ '55'  text repeated, not maths
int(n) * 2                               # ✅ 10
nums = list(map(int, input().split()))   # ✅ you type "3 4 5" → [3, 4, 5]
```

#### `len(x)`: how many?
```python
len("hello")     # 5
len([1, 2, 3])   # 3
len({"a": 1})    # 1   number of keys
len("")          # 0
len(5)           # ❌ TypeError: object of type 'int' has no len()
```

#### `range(start, stop, step)`: a run of whole numbers
**Takes:** **ints only** · **Gives back:** numbers from `start` up to, but **not including**, `stop`
```python
list(range(4))            # [0, 1, 2, 3]      stop is EXCLUDED
list(range(2, 5))         # [2, 3, 4]
list(range(0, 10, 3))     # [0, 3, 6, 9]
list(range(10, 0, -3))    # [10, 7, 4, 1]     negative step = count down
list(range(4, -1, -1))    # [4, 3, 2, 1, 0]   backwards over positions
list(range(5, 0))         # []   ← can't reach 0 by going UP: empty, NOT a crash
for i in range(len(nums)):    # ✅ the positions of a list
for i in range(nums):         # ❌ TypeError: 'list' object cannot be interpreted as an integer
range(2.5)                # ❌ TypeError: 'float' object cannot be interpreted as an integer
range(1, 5, 0)            # ❌ ValueError: range() arg 3 must not be zero
```

#### `sum(x)`: add everything up
```python
sum([3, 4, 5])     # 12
sum(range(4))      # 6   (0 + 1 + 2 + 3)
sum([])            # 0   ← empty is fine
sum(["a", "b"])    # ❌ TypeError: numbers only
```

#### `max()` / `min()`: biggest / smallest
```python
max([3, 9, 2])          # 9
min(4, 7)               # 4      also works with 2+ separate values
best = max(best, h)     # ✅ BEST SO FAR pattern
max("Zebra", "apple")   # 'apple'   ← lowercase counts as BIGGER
max([])                 # ❌ ValueError: max() iterable argument is empty
max([], default=0)      # ✅ 0   safe for an empty list
```
**Why `'apple'`?** Every character has a number (`ord("Z")` → `90`, `ord("a")` → `97`). Text is compared one character at a time, and **all uppercase letters come before all lowercase ones**. To ignore case, compare `.lower()` versions.

#### `sorted(x)`: a NEW sorted list
```python
sorted([3, 1, 2])                # [1, 2, 3]
sorted([3, 1, 2], reverse=True)  # [3, 2, 1]
sorted("cab")                    # ['a', 'b', 'c']   ← always a LIST, even from text
"".join(sorted("cab"))           # ✅ 'abc'   glue it back into text
nums = sorted(nums)              # ✅ keep the result
sorted(nums)                     # ❌ result thrown away, nums unchanged
sorted([1, "a"])                 # ❌ TypeError: '<' not supported between instances of 'str' and 'int'
```

#### `abs(x)`: distance from 0
```python
abs(-3)      # 3
abs(2.5)     # 2.5
abs("3")     # ❌ TypeError: bad operand type for abs(): 'str'
```

#### `round(x, digits)`
```python
round(3.7)          # 4
round(3.14159, 2)   # 3.14
round(2.5)          # 2   ← a tie (.5) goes to the EVEN number
round(3.5)          # 4   (4 is even)
round(-2.5)         # -2
round(4.5)          # 4   between 4 and 5: 4 is even
```
**Ties go to even** only for an exact `.5`: Python looks at the **two neighbours** and picks the even one (it isn't "even goes low, odd goes up"). **Why?** If every `.5` went up, adding thousands of rounded numbers would drift too high. Going to even sends half the ties up and half down, so they cancel out. Banks and statistics software use the same rule. 🔍 *Bookmarked to look into later.*

#### `//` vs `int()`: two different ways to lose the decimals
```python
int(-3.5)    # -3   CHOPS the decimal → moves toward 0
-7 // 2      # -4   rounds DOWN → moves LEFT on the number line
7 // 2       # 3    for positive numbers both look the same
```
```
  -5    -4   -3.5   -3    -2    -1    0
         ●←───┘                          // goes LEFT (down) → -4
              └───→●                     int() chops toward 0 → -3
```

#### `map(f, items)`: apply `f` to every item
**Gives back:** a lazy **map object**, not a list!
```python
map(int, ["1", "2"])            # ❌ <map object at 0x…>   can't see inside
list(map(int, ["1", "2"]))      # ✅ [1, 2]       text → numbers
" ".join(map(str, [1, 2]))      # ✅ '1 2'        numbers → text (for join)
m = map(int, ["1"]); m[0]       # ❌ TypeError: 'map' object is not subscriptable
```

#### `enumerate(x)`: position AND item together
```python
for i, ch in enumerate("hi"):
    print(i, ch)                # 0 h   then   1 i
list(enumerate("hi"))           # [(0, 'h'), (1, 'i')]
```

#### `reversed(x)`: back to front (doesn't change `x`)
```python
list(reversed([1, 2, 3]))   # ✅ [3, 2, 1]
"".join(reversed("abc"))    # ✅ 'cba'
"abc"[::-1]                 # ✅ 'cba'   the slice way
reversed([1, 2, 3])         # ❌ <list_reverseiterator …>   wrap it in list()
```

---

## 3. 🔤 String methods (after the dot: `s.upper()`)
> Strings can't change, so **every string method gives back NEW text**. Save it, or it's lost:
```python
s = "Hi"
s.upper()        # 'HI'   ❌ but s is still 'Hi' (result thrown away)
s = s.upper()    # ✅ now s is 'HI'
```

#### `.upper()` / `.lower()` / `.strip()`
```python
"hello".upper()        # 'HELLO'
"R".lower() == "r"     # ✅ True   lower both sides before comparing
"  hi  ".strip()       # 'hi'     spaces removed from BOTH ends (not the middle)
"--hi--".strip("-")    # 'hi'     strip other characters too
```

#### `.split()`: cut text into a list of pieces
Think of each separator as a **scissor cut**. Whatever sits between two cuts becomes one piece:
```
"a,,b"  →  a | (nothing) | b   →  ['a', '', 'b']    2 commas = 2 cuts = 3 pieces
```
```python
"3 4 5".split()             # ✅ ['3', '4', '5']   no argument = cut at ANY spaces
"  a  b ".split()           # ✅ ['a', 'b']         extra spaces ignored
"10,20,30".split(",")       # ✅ ['10', '20', '30']
"a,,b".split(",")           # ['a', '', 'b']        nothing between 2 commas = empty ''
"a, b".split(",")           # ❌ ['a', ' b']        the space sticks to 'b' → use .split(", ")
"a  b".split(" ")           # ❌ ['a', '', 'b']     2 spaces = 2 cuts → use .split()
"10,20".split(",")[0] + 5   # ❌ TypeError: pieces are TEXT → int(...) first
"x".split("")               # ❌ ValueError: empty separator
```
**Rule of thumb:** for input like `3 4 5`, always use `.split()` with **nothing inside**.

#### `sep.join(items)`: glue a list of TEXT into one string
```python
" ".join(["a", "b"])          # 'a b'
"".join(["a", "b"])           # 'ab'
", ".join(["x", "y"])         # 'x, y'
" ".join([1, 2])              # ❌ TypeError: sequence item 0: expected str instance, int found
" ".join(map(str, [1, 2]))    # ✅ '1 2'
["a", "b"].join(" ")          # ❌ AttributeError: 'list' object has no attribute 'join'  (glue goes FIRST)
```

#### `.replace(old, new)`
```python
"banana".replace("a", "o")      # 'bonono'   ALL matches
"banana".replace("a", "o", 1)   # 'bonana'   only the first 1
"banana".replace("x", "o")      # 'banana'   nothing found: no crash, no change
```

#### `.count(sub)`: how many times? (no overlaps)
```python
"banana".count("a")     # 3
"banana".count("ana")   # 1   ← after "ana" at 1–3, it carries on from 4 ("na")
"banana".count("x")     # 0
```

#### `.find(sub, start, end)`: WHERE is it? (`-1` = not there)
```python
"banana".find("na")         # 2    first match
"banana".find("na", 3)      # 4    start looking at position 3
"banana".find("na", 0, 3)   # -1   only looks inside "ban"
"banana".find("x")          # -1   not found: NO crash
```

#### `.index(sub)`: like `find`, but crashes
```python
"banana".index("n")    # 2
"banana".index("x")    # ❌ ValueError: substring not found   → use .find() or `in`
```

#### `in`, `.startswith()`, `.endswith()`: yes / no
```python
"ana" in "banana"            # True
"Ana" in "banana"            # False   case matters
"hello".startswith("he")     # True
"hello".endswith("lo")       # True
```

#### `.isdigit()` / `.isalpha()`
```python
"123".isdigit()    # True
"12.5".isdigit()   # False   the dot isn't a digit
"-5".isdigit()     # False   the minus isn't a digit
"abc".isalpha()    # True
"ab c".isalpha()   # False   the space isn't a letter
```

#### `s[i]` and slices `s[start:stop:step]`
```python
s = "python"
s[0], s[-1]       # 'p' 'n'
s[1:4]            # 'yth'      stop excluded
s[::2]            # 'pto'      every 2nd
s[::-1]           # 'nohtyp'   reversed
s[10]             # ❌ IndexError: string index out of range
s[0] = "P"        # ❌ TypeError: 'str' object does not support item assignment
s = "P" + s[1:]   # ✅ 'Python'   build a new one instead
```

---

## 4. 📋 List methods
> List methods **change the list itself** and mostly give back **`None`**:
```python
x = [3, 1]
x = x.append(5)   # ❌ now x is None!   (append gave back None, and you saved it)
x.append(5)       # ✅ x is [3, 1, 5]
```

#### Adding: `.append()`, `.extend()`, `.insert()`
```python
x = [1, 2]
x.append(3)           # x = [1, 2, 3]
x.append([4, 5])      # x = [1, 2, 3, [4, 5]]   ← ONE item (a list inside a list)

x = [1, 2]
x.extend([3, 4])      # x = [1, 2, 3, 4]        each item added
x.extend("ab")        # x = [1, 2, 3, 4, 'a', 'b']   a string = its letters

x = ["a", "c"]
x.insert(1, "b")      # x = ['a', 'b', 'c']     POSITION first, then the value
x.insert(0, "z")      # x = ['z', 'a', 'b', 'c']   at the front
x.insert(99, "end")   # added at the end (a too-big position doesn't crash)
x.insert("b")         # ❌ TypeError: insert expected 2 arguments, got 1
```

#### Removing: `.pop()` (by POSITION) vs `.remove()` (by VALUE) vs `del`
```python
x = [10, 20, 30]
x.pop()               # 30   gives back the LAST → x = [10, 20]
x.pop(0)              # 10   position 0 = the first → x = [20]
picked = x.pop()      # ✅ save what it gives back → picked = 20, x = []
x.pop()               # ❌ IndexError: pop from empty list
x = [5, 9]
x.pop(9)              # ❌ IndexError: pop index out of range   (pop wants a POSITION, not the value 9)

x = [3, 5, 3]
x.remove(3)           # x = [5, 3]   removes the FIRST 3 (a value); gives back None
x.remove(99)          # ❌ ValueError: list.remove(x): x not in list
if 99 in x:           # ✅ check first
    x.remove(99)

x = [10, 20, 30]
del x[1]              # x = [10, 30]   by position, gives back nothing
```

#### Looking: `.index()`, `.count()`, `in`
```python
[5, 6, 5].index(5)   # 0      the first POSITION of that value
[5, 6, 5].count(5)   # 2
3 in [1, 2, 3]       # True   checks VALUES
[5, 6].index(9)      # ❌ ValueError: 9 is not in list
```

#### Ordering: `.sort()` / `.reverse()` (in place, give back `None`)
```python
x = [3, 1, 2]
x.sort()               # x = [1, 2, 3]
x.sort(reverse=True)   # x = [3, 2, 1]
x.reverse()            # x = [1, 2, 3]   flips it
y = x.sort()           # ❌ y is None
y = sorted(x)          # ✅ a NEW sorted list (the function, not the method)
```

#### Replacing by position: `x[i] = v`
```python
x = [0] * 3       # [0, 0, 0]   3 slots
x[1] = 7          # [0, 7, 0]   replaces slot 1 only
ans = []
ans[0] = 5        # ❌ IndexError: list assignment index out of range   (can't grow a list this way)
ans.append(5)     # ✅ [5]
```

#### Joining and repeating: `+` and `*` (give back a NEW list)
```python
[1, 2] + [3]      # [1, 2, 3]
[0] * 3           # [0, 0, 0]
[1] + [2]         # ✅ [1, 2]
[1] + 2           # ❌ TypeError: can only concatenate list (not "int") to list
```

---

## 5. 📖 Dictionaries

#### Reading a value
```python
d = {"a": 1}
d["a"]             # 1
d["z"]             # ❌ KeyError: 'z'
d.get("z")         # None   safe: no crash
d.get("z", 0)      # 0      safe, with your own fallback
```

#### Adding and changing
```python
d = {"a": 1}
d["b"] = 2                    # adds:       {'a': 1, 'b': 2}
d["a"] = 5                    # overwrites: {'a': 5, 'b': 2}
d["c"] += 1                   # ❌ KeyError: 'c'   there's no old value to add to
d["c"] = d.get("c", 0) + 1    # ✅ the COUNTING pattern → {'a': 5, 'b': 2, 'c': 1}
d[[1, 2]] = 3                 # ❌ TypeError: unhashable type: 'list'   (a list can't be a key)
```

#### Removing
```python
d = {"a": 5, "b": 2}
d.pop("a")         # 5   gives back the removed VALUE → d = {'b': 2}
del d["b"]         # d = {}
d.pop("q")         # ❌ KeyError: 'q'
```

#### Checking and looping
```python
d = {"a": 1, "b": 2}
"a" in d                   # True    checks KEYS only
1 in d                     # False   ← 1 is a value, not a key
len(d)                     # 2       number of keys
for k in d:                # keys:   'a', 'b'
for v in d.values():       # values: 1, 2
for k, v in d.items():     # pairs:  ('a', 1), ('b', 2)
```

---

## 6. ➗ Operators: what they do depends on the type

#### Numbers
```python
7 + 2, 7 - 2, 7 * 2   # 9 5 14
7 / 2                 # 3.5
7 / 7                 # 1.0    / ALWAYS gives a float
7 // 2                # 3      divide, then round DOWN
-7 // 2               # -4     ← DOWN means toward −∞ (see the number line)
7 % 2                 # 1      the remainder
-7 % 2                # 1
n % 2 == 0            # ✅ the "is it even?" test
2 ** 3                # 8      power
2 ** 0.5              # 1.4142135623730951   square root
n = 1234
n % 10                # 4      ✅ the LAST digit (remainder after dividing by 10)
n // 10               # 123    ✅ DROP the last digit
n.pop()               # ❌ AttributeError: 'int' object has no attribute 'pop'   (.pop() is for lists)
```
```
   -4 ←──── -3.5 ────→ -3
  ✅ //       (/)        ❌ not this
 "down" on the number line is always to the LEFT
```

#### Text and lists
```python
"ab" + "c"     # 'abc'      join (both sides the same type)
"ab" * 3       # 'ababab'   repeat with an int
[0] * 3        # [0, 0, 0]
"ab" + 3       # ❌ TypeError: can only concatenate str (not "int") to str
[1] + 2        # ❌ TypeError: can only concatenate list (not "int") to list
"ab" * "2"     # ❌ TypeError: can't multiply sequence by non-int of type 'str'
"ab" - "b"     # ❌ TypeError: unsupported operand type(s) for -: 'str' and 'str'
```

#### Comparing (`== != < > <= >=` give back `True`/`False`)
```python
3 == 3.0             # True
"3" == 3             # False   text is never equal to a number (no crash)
"apple" < "banana"   # True    character by character
"Zebra" < "apple"    # True    uppercase first (Z = 90 < a = 97)
"3" < 3              # ❌ TypeError: '<' not supported between instances of 'str' and 'int'
x = 5                # =  STORES
x == 5               # == COMPARES → True
```

#### Combining: `and`, `or`, `not`
```python
age = 20
age >= 18 and age < 60   # True    both must be True
18 <= age < 60           # ✅ True  same thing, shorter
age < 5 or age > 60      # False   at least one must be True
not True                 # False
```

---

## 7. 🚨 Error decoder: what each crash means
**Which one is it?** Ask in this order:
1. Can Python even **read** the line? No → `SyntaxError`
2. Is it the wrong **kind** of thing (text where a number should be, a list where an int should be)? → `TypeError`
3. Right kind of thing, but bad **content** (`"12.5"` is text, but not *whole-number* text)? → `ValueError`
4. A **position** that doesn't exist? → `IndexError` · a **key** that doesn't exist? → `KeyError`

| Error | Meaning | My examples |
|---|---|---|
| `SyntaxError` | Python can't read the line | missing `:`, `elif elif`, `range(1:n)`, `return` outside a function |
| `TypeError` | wrong **type** for this operation | `"12" + 3`, `[1] + 2`, `range(list)`, `len(5)`, `",".join([1, 2])` |
| `ValueError` | right type, **bad value** | `int("12.5")`, `x.remove(99)`, `max([])` |
| `IndexError` | position doesn't exist | `ans[0] = 5` on `[]`, `[].pop()`, `a.pop(a[0])` |
| `KeyError` | key doesn't exist | `d["z"] += 1` on a new key |
| `AttributeError` | that type has no such method | `map(...).sort()`, `scores.max()`, `["a"].join(" ")` |
| `NameError` | name never created (or a typo) | using a variable before assigning it |
| `ZeroDivisionError` | divided by 0 | `average([])` |
| "Time Limit Exceeded" | the loop never ends (or is too slow) | `while` loop that never moves (LeetCode 344) |

### ✅ These look scary but do NOT crash
```python
"banana"[2:100]           # 'nana'      slices stop at the end
"banana"[10:]             # ''
"abc"[5]                  # ❌ but THIS one crashes: one position = IndexError
list(range(3, 3))         # []          start = stop → nothing (stop is excluded)
int(" 8 ")                # 8           spaces at the ends are fine
list(range(5, 0))         # []          can't reach the stop → empty
"banana".find("x")        # -1          "not found" is an answer
"banana".replace("x", "o")   # 'banana'  nothing to replace
d.get("missing")          # None
sum([])                   # 0
x.insert(99, "v")         # adds at the end
"3" == 3                  # False
print("a", "b", 3)        # a b 3       numbers need no quotes
```
