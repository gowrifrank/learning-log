# 📘 Day 08: Tuples & Sets 🧺
Two new containers, next to lists and dictionaries:
- A **tuple** is like a list that **can't be changed** after you make it.
- A **set** is a bag of **unique** items, so there are no duplicates and no positions.

---

# Part A: Tuples `( )`

## 1. Creating and reading
```python
point = (3, 4)
print(point[0])        # 3   (positions work, like a list)
print(len(point))      # 2
print(point[-1])       # 4

point[0] = 10          # ❌ TypeError: 'tuple' object does not support item assignment
```
- Round brackets `( )` with items separated by commas
- You can **read** by position and slice, but you can **never change, add or remove** items
- One item needs a comma: `(5,)` is a tuple, but `(5)` is just the number 5 in brackets

## 2. Unpacking ⭐ (the most useful tuple trick)
Unpacking puts each item into its own variable in one line:
```python
point = (3, 4)
x, y = point           # x = 3, y = 4
print(x, y)            # 3 4

a, b = 5, 9            # the right side is a tuple, even without brackets
a, b = b, a            # SWAP in one line: a = 9, b = 5
```
The number of variables on the left must match the number of items, or you get `ValueError: too many values to unpack`.

**You've already used this!** In Day 07, `for key, value in robot.items():` works because `.items()` gives **tuples** like `("name", "Optimus")`, and the `for` unpacks each one.

## 3. Returning two values from a function
```python
def first_and_last(word):
    return word[0], word[-1]        # actually returns ONE tuple: ('p', 'n')

f, l = first_and_last("python")     # unpack it straight away
print(f, l)                         # p n
```

## 4. Tuple or list?
| Use a **list** `[ ]` when... | Use a **tuple** `( )` when... |
|---|---|
| the items will change (add, remove, sort) | the group is fixed: a point `(x, y)`, a date `(2026, 11, 16)` |
| it's a collection of similar things | it's one "record" with a fixed shape |

---

# Part B: Sets `{ }`

## 5. Creating: duplicates disappear
```python
colours = {"red", "blue", "red", "green"}
print(colours)            # {'red', 'blue', 'green'}  (order may differ!)
print(len(colours))       # 3: the second "red" was dropped

nums = set([3, 1, 3, 2, 1])
print(nums)               # {1, 2, 3}
print(set("banana"))      # {'b', 'a', 'n'}: a set of the letters

empty = set()             # ✅ an empty set
empty = {}                # ❌ that's an empty DICTIONARY, not a set!
```
- **No duplicates**: each item appears at most once
- **No order, no positions**: `colours[0]` gives ❌ `TypeError: 'set' object is not subscriptable`

## 6. Adding, removing, checking
```python
s = {1, 2, 3}
s.add(4)              # {1, 2, 3, 4}
s.add(2)              # still {1, 2, 3, 4}: 2 was already there
s.remove(1)           # {2, 3, 4}
s.remove(99)          # ❌ KeyError: 99 (it isn't there)
s.discard(99)         # no crash: discard ignores missing items
print(3 in s)         # True, and this check is VERY fast in a set
```

## 7. Set maths: comparing two groups ⭐
```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
```
| Question | Operator | Method | Result |
|---|---|---|---|
| In **either** one (all items)? | `a \| b` | `a.union(b)` | `{1, 2, 3, 4, 5}` |
| In **both**? | `a & b` | `a.intersection(b)` | `{3, 4}` |
| In `a` but **not** in `b`? | `a - b` | `a.difference(b)` | `{1, 2}` |
| In **exactly one** (not both)? | `a ^ b` | `a.symmetric_difference(b)` | `{1, 2, 5}` |

Picture two overlapping circles: `&` is the overlap, `|` is everything, `-` is one circle minus the overlap, and `^` is everything except the overlap.

## 8. Two patterns you'll use constantly
**Count unique items:**
```python
words = "the cat and the hat".split()
print(len(set(words)))        # 4 unique words (the second "the" is dropped)
```
(Remember LeetCode 1832 Pangram: `len(set(sentence)) == 26` is this exact trick.)

**"Have I seen this before?"**
```python
seen = set()
for n in [4, 7, 2, 7, 9]:
    if n in seen:
        print("Repeat:", n)       # Repeat: 7
        break
    seen.add(n)
```
Start an empty set, check `in`, then `add`. It's the same shape as the Day 07 COUNTING pattern, but you only care whether you've seen it, not how many times.

---

## All four containers
| | List `[ ]` | Tuple `( )` | Set `{ }` | Dict `{k: v}` |
|---|---|---|---|---|
| Can change? | ✅ | ❌ | ✅ | ✅ |
| Duplicates? | ✅ | ✅ | ❌ | keys ❌ |
| Find items by | position | position | `in` only | key |
| Best for | a changing sequence | a fixed record | unique items, fast `in` | labelled lookups, counting |

---

## ✍️ Exercise: `day08.py`
Do **Part A (1–3) first** and show me. Then do Part B (4–6).

**Part A: tuples**
1. **Point:** make `point = (7, 2)`. Unpack it into `x` and `y` and print `x = 7, y = 2`. Then try `point[0] = 1`, read the error, and comment that line out with `#`.
2. **Swap:** `a = 5` and `b = 9`. Swap them **in one line** and print both.
3. **Min and max:** write `def min_max(nums):` that **returns** the smallest and the biggest number together. Call it with `[8, 3, 11, 5]` and unpack the answer: `low, high = ...`. Print `3 11`.

**Part B: sets**

4. **Unique words:** ask for a sentence with `input()`. Print how many words it has, and how many **different** words.
5. **Two friends:** `me = {"chess", "music", "cricket", "coding"}` and `friend = {"music", "coding", "football"}`. Print the hobbies you **share**, **all** hobbies, the ones **only you** have, and the ones only **one** of you has.
6. **First repeat:** given `nums = [5, 1, 8, 1, 5, 3]`, use the "seen before?" pattern to print the **first number that repeats** (answer: `1`).

**Bonus 🧠:** LeetCode **217. Contains Duplicate**: return `True` if any number appears twice. Try it with the "seen before?" pattern, then in **one line** with `len` and `set`.

---

## 🔥 HackerRank: [Introduction to Sets](https://www.hackerrank.com/challenges/py-introduction-to-sets/problem)
Find the **average of the distinct heights**: count each height only once.

**Hints:**
- `set(array)` drops the repeated heights
- Then `sum(...) / len(...)` of that set, as in Day 07's Finding the Percentage
- HackerRank's starter code prints the result for you, so just `return` the average
