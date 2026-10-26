# 📕 The Add · Remove · Loop Book
> My weak spot, attacked one chapter at a time: **putting things into, taking things out of, and walking through** lists, dictionaries and strings.
> **How to use it:** 3 drills from the 🏋 sections at the start of every session (answers are at the bottom, so cover them up!). A new chapter gets added whenever a problem trips me up.
> Companion to [data-structures-guide.md](data-structures-guide.md), which covers parsing input and printing.

---

## 0. The one question that fixes most bugs
Before touching a list, ask: **"Do I mean a POSITION or a VALUE?"**

```
cubes  =  [ 4,  3,  2,  1 ]
position:   0   1   2   3      ← where it sits (cubes[0])
value:      4   3   2   1      ← what it is
```

| Wants a **position** | Wants a **value** |
|---|---|
| `lst[i]` | `x in lst` |
| `lst.pop(i)` | `lst.remove(x)` |
| `lst.insert(i, x)` (i = where) | `lst.append(x)` (x = what) |
| `del lst[i]` | `lst.count(x)` |
| `range(len(lst))` gives positions | `lst.index(x)` gives back a position |

🔁 **My repeat offenders:** `pop(blocks[0])` (Piling Up), `output[value - 1]` (1480), `range(list)` (1672, Piling Up).

---

## 1. 📋 Lists

### Add
| Code | What happens | Gives back |
|---|---|---|
| `lst.append(x)` | puts x at the **end** | `None` |
| `lst.insert(i, x)` | puts x **at position i**, pushes the rest right | `None` |
| `lst + [x, y]` | makes a **new** list, glued together | the new list |
| `lst.extend([x, y])` | adds each item to the end | `None` |

### Remove
| Code | What happens | Gives back |
|---|---|---|
| `lst.pop()` | removes the **last** item | **that item** ✅ |
| `lst.pop(0)` | removes the **first** item | **that item** ✅ |
| `lst.pop(i)` | removes the item **at position i** | **that item** ✅ |
| `lst.remove(x)` | removes the **first item equal to x** | `None` |
| `del lst[i]` | removes the item at position i | nothing (it's a statement) |

### Look / change
| Code | Meaning |
|---|---|
| `lst[0]`, `lst[-1]` | first, last |
| `lst[len(lst) - 1]` | last, the long way (same as `lst[-1]`) |
| `lst[i] = x` | replace what's at position i |
| `lst[a:b]` | a **copy** of positions a … b-1 |

### ⚠️ Traps
1. **`lst = lst.append(x)`** → lst becomes `None`! `append` changes the list *in place* and gives back nothing. Just write `lst.append(x)`.
2. **`print(lst.sort())`** prints `None` for the same reason. Use `print(sorted(lst))`, or `lst.sort()` and then `print(lst)`.
3. **Removing while looping over the same list** skips items. Loop with `while lst:` instead, or build a new list (FILTER pattern).
4. **`pop()` on an empty list** → `IndexError: pop from empty list`. Check `if lst:` first.

### 🏋 Drills: lists (predict the output, then run it)
```python
# L1
a = [10, 20, 30]
a.append(40)
print(a)

# L2
a = [10, 20, 30]
x = a.pop(0)
print(x, a)

# L3
a = [10, 20, 30]
a.insert(1, 99)
print(a)

# L4
a = [5, 3, 5, 1]
a.remove(5)
print(a)

# L5
a = [4, 3, 2]
a = a.append(1)
print(a)

# L6
a = [4, 3, 2, 1]
print(a.pop(a[0]))          # careful!
```

---

## 2. 🔁 Walking through a list: 4 ways
| I need… | Write | Each round gives me |
|---|---|---|
| just the items | `for x in lst:` | the value |
| positions (to look left/right, or change `lst[i]`) | `for i in range(len(lst)):` | the position |
| both | `for i, x in enumerate(lst):` | position **and** value |
| to eat it from the ends | `while lst:` + `lst.pop()` / `lst.pop(0)` | whatever you pop |
| two ends moving inwards | `left, right = 0, len(lst) - 1` + `while left <= right:` | two positions |

### 🏋 Drills: loops
```python
# W1: what's printed?
for i in range(len(["a", "b", "c"])):
    print(i)

# W2: what's printed?
for i, x in enumerate(["a", "b"]):
    print(i, x)

# W3: what's printed?
s = [1, 2, 3]
while s:
    print(s.pop())

# W4: fix the bug
nums = [3, 1, 2]
for i in range(nums):
    print(nums[i])
```

---

## 3. 📖 Dictionaries
A dictionary maps a **key → value**. There are no positions, **only keys**.

### Add / change / remove / look
| Code | What happens |
|---|---|
| `d[key] = value` | adds the key, or **overwrites** it if it exists |
| `d[key] += 1` | ⚠️ crashes with `KeyError` if the key isn't there yet |
| `d[key] = d.get(key, 0) + 1` | the **COUNTING** line: safe even for a new key |
| `d[key]` | look up (⚠️ `KeyError` if missing) |
| `d.get(key, default)` | look up, with no crash |
| `key in d` | checks **keys**, not values |
| `d.pop(key)` | removes the key and **gives back its value** |
| `del d[key]` | removes the key |

### Walking through
| I need… | Write |
|---|---|
| keys | `for k in d:` |
| values | `for v in d.values():` |
| both | `for k, v in d.items():` |
| keys in order | `for k in sorted(d):` |

### 🏋 Drills: dictionaries
```python
# D1
d = {}
d["a"] = 1
d["a"] = 5
print(d)

# D2
d = {"x": 1}
print("x" in d, 1 in d)

# D3
counts = {}
for ch in "banana":
    counts[ch] = counts.get(ch, 0) + 1
print(counts)

# D4
d = {"a": 1, "b": 2}
v = d.pop("a")
print(v, d)

# D5: what happens?
d = {}
d["z"] += 1
```

---

## 4. 🔤 Strings: you can't change them, only rebuild
Strings are **frozen** (*immutable*): `s[0] = "X"` crashes. To "add" or "remove", you build a **new** string.

| Want | Write |
|---|---|
| add to the end | `s = s + "x"` or `s += "x"` |
| remove the first char | `s = s[1:]` |
| remove the last char | `s = s[:-1]` |
| list of words | `s.split()` |
| words → one string | `" ".join(words)` |
| list of characters | `list(s)` |

### 🏋 Drills: strings
```python
# S1
s = "cat"
s += "s"
print(s)

# S2
print("hello"[1:-1])

# S3
print("-".join(["a", "b", "c"]))
```

---

## 5. 🗺 `map`: do the same thing to every item
`map(f, items)` = "apply **f** to each item". It gives back a lazy *map object*, so wrap it in `list(...)` to see it.

```python
words = "4 3 2".split()          # ['4', '3', '2']   ← strings!
nums  = list(map(int, words))    # [4, 3, 2]          ← numbers
```
It's the same as this loop:
```python
nums = []
for w in words:
    nums.append(int(w))
```

### 🏋 Drills: map
```python
# M1
print(list(map(int, "7 8 9".split())))

# M2
print(list(map(len, ["hi", "hello"])))

# M3: what's printed (and why is it odd)?
print(map(int, ["1", "2"]))
```

---

## 6. 📒 Chapters added from real problems
| Problem | What tripped me | Chapter |
|---|---|---|
| HackerRank Piling Up! (26 Oct) | `pop(value)` instead of `pop(position)`; `range(list)` | §0, §1 |
| LeetCode 1672 (24 Oct) | `range(list)` | §2 |
| HackerRank Merge the Tools (23 Oct) | rebuilding a string per piece | §4 |
| LeetCode 2149 (22 Oct) | mixing positions of two lists of different sizes | §0 |
| HackerRank Word Order (22 Oct) | counting letters instead of words | §3 |

---

## ✅ Answers (cover these up!)
<details><summary>Click to reveal</summary>

- **L1** `[10, 20, 30, 40]`
- **L2** `10 [20, 30]`
- **L3** `[10, 99, 20, 30]`
- **L4** `[3, 5, 1]`: only the **first** 5 goes
- **L5** `None`: `append` gives back nothing
- **L6** `IndexError`: `a[0]` is 4, so it tries `pop(4)`, but the last position is 3
- **W1** `0 1 2` (one per line)
- **W2** `0 a` then `1 b`
- **W3** `3 2 1`: pop takes from the end
- **W4** `range(len(nums))`
- **D1** `{'a': 5}`: same key, overwritten
- **D2** `True False`: `in` checks keys only
- **D3** `{'b': 1, 'a': 3, 'n': 2}`
- **D4** `1 {'b': 2}`
- **D5** `KeyError: 'z'`: use `d.get("z", 0) + 1`
- **S1** `cats`
- **S2** `ell`
- **S3** `a-b-c`
- **M1** `[7, 8, 9]`
- **M2** `[2, 5]`
- **M3** `<map object at 0x...>`: needs `list(...)` around it
</details>
