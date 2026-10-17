# 📘 Day 07: Dictionaries 📖
A **dictionary** stores **pairs**: a **key** → a **value**. You look things up by **name** instead of by position, just like a real dictionary (word → meaning) or a phone book (name → number).

## 1. Creating and reading
```python
robot = {
    "name": "Optimus",
    "maker": "Tesla",
    "year": 2022,
}
print(robot["name"])        # Optimus  (look up by KEY, not position)
print(len(robot))           # 3 pairs
```
- `{ }` with `key: value` pairs, separated by commas
- Keys are usually strings, and values can be anything (numbers, strings, lists...)

## 2. Missing keys: `[]` vs `.get()`
```python
print(robot["price"])           # ❌ KeyError: 'price'
print(robot.get("price"))       # None, no crash
print(robot.get("price", 0))    # 0, your own default
print("price" in robot)         # False, checks KEYS
```

## 3. Adding, changing, deleting
```python
robot["price"] = 20000      # add a new pair
robot["year"] = 2024        # change an existing value (same syntax!)
del robot["maker"]          # delete a pair
```
Dictionaries **can be changed**, like lists.

## 4. Looping
```python
for key in robot:                   # loops over KEYS
    print(key)

for value in robot.values():        # just the values
    print(value)

for key, value in robot.items():    # BOTH at once ⭐ the most useful
    print(f"{key}: {value}")
```

## 5. The COUNTING pattern ⭐ (you'll use this constantly)
```python
word = "banana"
counts = {}                         # start empty (ACCUMULATOR!)
for ch in word:
    if ch in counts:
        counts[ch] += 1             # seen before: add 1
    else:
        counts[ch] = 1              # first time: start at 1
print(counts)                       # {'b': 1, 'a': 3, 'n': 2}
```
Shorter, using `.get()` with a default:
```python
for ch in word:
    counts[ch] = counts.get(ch, 0) + 1
```

## 6. Lists inside dictionaries
```python
marks = {
    "Gowri": [85, 92, 78],
    "Optimus": [99, 100, 98],
}
print(marks["Gowri"][1])                         # 92
print(sum(marks["Gowri"]) / len(marks["Gowri"])) # average of Gowri's marks
```

## Lists vs dictionaries
| | List `[ ]` | Dictionary `{ }` |
|---|---|---|
| Find items by | **position** `x[0]` | **key** `x["name"]` |
| Order matters? | yes | keeps insertion order, but you look things up by key |
| Best for | a sequence of similar things | **labelled** data, lookups, counting |

---

## ✍️ Exercise: `day07.py`
1. **Robot profile:** make a dictionary for your favourite robot (name, maker, year, height). Print each pair with `.items()`, add a `"price"`, change the `year`, and delete one key.
2. **Phone book:** a dictionary of 3 names → numbers. Ask the user for a name and print the number, or `"Not found"` if it's missing (use `.get()` or `in`, with **no crash**).
3. **Letter counter:** ask for a word and count each letter with the COUNTING pattern. Then print the **most common letter**. *(Hint: loop over `.items()` and keep the BEST SO FAR, like second-highest!)*
4. **Grade book:** `scores = {"Gowri": 92, "Atlas": 74, "ASIMO": 58, "Spot": 81}`. **Reuse your Day 06 `grade()` function** to print each name with their grade: `Gowri: A`.

**Bonus 🧠 (LeetCode preview!):** given `nums = [2, 7, 11, 15]` and `target = 9`, find the **two positions** whose numbers add up to the target (answer: `0, 1`, because 2 + 7 = 9).
*Hint:* as you loop, store each number you've seen in a dictionary `{number: position}`. For each new number, check whether `target - number` is already in the dictionary. This is **LeetCode problem #1, "Two Sum"**, the most famous interview problem!

---

## 🔥 HackerRank: [Finding the percentage](https://www.hackerrank.com/challenges/finding-the-percentage/problem)
They give you a dictionary of `name → list of marks`. Print the **average** of one student's marks, with **2 decimal places**.

**Hints:**
- Their starter code already builds the dictionary `student_marks` for you
- Look up the student's list, then `sum(...) / len(...)` (Day 05 + Day 06!)
- 2 decimals: `print(f"{avg:.2f}")`. The `:.2f` inside the f-string means "2 digits after the point". That's new and useful!
