# 🗂 Data Structures Guide: Lists, Strings, Dictionaries & Parsing Input
> ⭐ **My weak spot.** Read this before every HackerRank / LeetCode problem until it feels natural.
> Golden rule: **always know WHAT you're holding.** Is it a string? A list? A dictionary? A list *inside* a dictionary?
> 📕 **Adding, removing and looping** (append/pop/insert/remove, dict add/remove, `map`) now has its own drill book: [add-remove-loop-book.md](add-remove-loop-book.md).

---

## 1. The 3 containers at a glance
| | String `"..."` | List `[...]` | Dictionary `{...}` |
|---|---|---|---|
| Holds | characters | any items, in order | **key → value** pairs |
| Example | `"Harsh"` | `[25.0, 26.5, 28.0]` | `{"Harsh": [25.0, 26.5, 28.0]}` |
| Get one item | `s[0]` → `"H"` | `x[0]` → `25.0` | `d["Harsh"]` → `[25.0, 26.5, 28.0]` |
| By | position | position | **key** (name) |
| Can change? | ❌ no | ✅ yes | ✅ yes |
| Length | `len(s)` | `len(x)` | `len(d)` (number of pairs) |
| Check inside | `"H" in s` | `25.0 in x` | `"Harsh" in d` (checks **keys**) |

---

## 2. 🔍 "What am I holding?" Print it!
When confused, **print the variable and its type**. This is the #1 debugging trick:
```python
print(student_marks)          # {'Harsh': [25.0, 26.5, 28.0], 'Anurag': [26.0, 28.0, 30.0]}
print(type(student_marks))    # <class 'dict'>
print(type(student_marks["Harsh"]))     # <class 'list'>
print(type(student_marks["Harsh"][0]))  # <class 'float'>
```

---

## 3. 🪜 Going down layers (nested data)
Read nested access **left to right, one step at a time**:
```python
student_marks = {"Harsh": [25.0, 26.5, 28.0], "Anurag": [26.0, 28.0, 30.0]}

student_marks                  # the whole dictionary
student_marks["Harsh"]         # step 1: open the "Harsh" drawer → [25.0, 26.5, 28.0]
student_marks["Harsh"][1]      # step 2: second item in that list → 26.5
```
Like an address: **cupboard → drawer → item**.

---

## 4. 🔁 Looping over each container
| Loop | Gives you | Example |
|---|---|---|
| `for ch in "hi":` | each **character** | `h`, `i` |
| `for x in [10, 20]:` | each **item** | `10`, `20` |
| `for i in range(len(lst)):` | each **position** | `0`, `1`, then use `lst[i]` |
| `for key in d:` | each **key** | `"Harsh"`, `"Anurag"` |
| `for value in d.values():` | each **value** | `[25.0, ...]`, `[26.0, ...]` |
| `for key, value in d.items():` | **both** ⭐ | `"Harsh"`, `[25.0, ...]` |

🔑 **Name the loop variable after what it IS:** `ch`, `num`, `name`, `marks`. Use `i` only for positions.

⚠️ **The loop variable keeps its LAST value after the loop ends:**
```python
for name in ["Harsh", "Anurag"]:
    pass
print(name)       # "Anurag", the last one! (this caused my "Finding the percentage" bug)
```

---

## 5. 📥 Parsing input (HackerRank's favourite)
Input always arrives as **text**. Turning it into numbers and containers is called **parsing**.

### One number
```python
n = int(input())                      # "3" → 3
```

### Many numbers on one line
```python
nums = list(map(int, input().split()))
```
Read it **inside → out** with input `"2 3 6"`:
| Step | Code | Result |
|---|---|---|
| 1 | `input()` | `"2 3 6"` (one string) |
| 2 | `.split()` | `["2", "3", "6"]` (list of strings) |
| 3 | `map(int, ...)` | applies `int()` to each (a lazy "recipe") |
| 4 | `list(...)` | `[2, 3, 6]` (real list of numbers) ✅ |

Use `float` instead of `int` for decimals: `list(map(float, ...))` → `[25.0, 26.5]`.
Same thing without `map` (a list comprehension, coming soon): `[int(x) for x in input().split()]`

### A name followed by numbers
```python
name, *rest = "Harsh 25 26.5 28".split()
# name = "Harsh"
# rest = ["25", "26.5", "28"]     (* = "collect everything else into a list")
scores = list(map(float, rest))   # [25.0, 26.5, 28.0]
```

### Many lines → a dictionary
```python
student_marks = {}
for _ in range(n):                 # _ = "I don't need the counter, just repeat n times"
    name, *line = input().split()
    student_marks[name] = list(map(float, line))
```

---

## 6. 🖨 Printing
```python
x = [1, 2, 3]
print(x)                     # [1, 2, 3]       (the whole list, with brackets)
print(*x)                    # 1 2 3           (* "unpacks" the items, separated by spaces)
print(*x, sep=",")           # 1,2,3
for item in x:
    print(item)              # one per line

d = {"a": 1, "b": 2}
for key, value in d.items():
    print(f"{key}: {value}") # a: 1   b: 2

avg = 26.5
print(f"{avg:.2f}")          # 26.50 (2 decimal places)
```

---

## 7. 🧰 The patterns that cover 80% of problems
| Pattern | Container | Code shape |
|---|---|---|
| ACCUMULATOR | number | `total = 0` → `total += x` |
| BUILD A LIST | list | `result = []` → `result.append(x)` |
| FILTER | list | `if condition: result.append(x)` |
| COUNTING | dict | `counts[x] = counts.get(x, 0) + 1` |
| LOOKUP | dict | `d[key]` or `d.get(key, default)` |
| BEST SO FAR | any | `best = None` → `if best is None or x > best: best = x` |

---

## 8. ✅ Before submitting: data checklist
- [ ] Did I **print** the data once to see its real shape?
- [ ] Am I using the **right variable**? (e.g. `query_name`, not a leftover loop variable)
- [ ] Is it **text or a number**? Do I need `int()` / `float()`?
- [ ] Am I getting **items, positions or keys** from this loop?
- [ ] Am I using the data **after** it's been read? (order of lines matters!)
