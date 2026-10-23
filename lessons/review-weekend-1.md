# 🔁 Big Review #1: Sat 24 + Sun 25 Oct 2026
> Goal: make **strings, searching, printing, items vs positions, `map` and dictionaries** feel automatic.
> These are my own weak spots (said on 23 Oct). Everything here comes from **my** lessons, problems and mistakes.

**How each block works (about 1.5–2 h per day, take breaks):**
1. 📖 **Reread** (10 min): the listed notes. Read, don't copy.
2. 🧠 **Predict** (20 min): for each drill, write what it prints **before** running it. Then check in VS Code (`review.py`, a scratch file).
3. ✍️ **Rewrite from memory** (40 min): solve old problems again **without looking**. Stuck for 5 min? Peek at one line only.
4. 💡 **Better ways** (15 min): read the matching sections in [approaches.md](../approaches.md).
5. 🟢 **One Easy LeetCode** to keep the streak. Then commit.

Mark each drill ✅ (right first time), 🟡 (right after thinking) or ❌ (wrong). The ❌ ones go to [quiz-log.md](../quiz-log.md)'s retry list.

---

## 📅 Saturday: Strings, searching, printing, items vs positions

### 📖 Reread
- [notes.md](../notes.md): Day 03 (loops), Day 04 (strings), "print tricks"
- [data-structures-guide.md](data-structures-guide.md) sections 2, 4 and 6
- [mistakes-journal.md](../mistakes-journal.md): focus area 1 (items vs positions)

### 🧠 Predict the output
```python
s = "banana"
# S1
print(s[1], s[-1], s[1:4])
# S2
print(s.find("n"), s.find("z"))
# S3
print(s.count("a"), "nan" in s, "N" in s)
# S4
s.upper()
print(s)
# S5
print("a-b-c".split("-"))
# S6
print("-".join(["x", "y", "z"]))
# S7
for ch in "abc":
    print(ch, end=" ")
# S8
for i in range(len("abc")):
    print(i, end=" ")
# S9
nums = [5, 7, 9]
for i in range(len(nums)):
    print(i, nums[i])
# S10
print(1, 2, 3, sep=", ")
# S11
print("A", end="")
print("B")
# S12
result = ""
for ch in "hello":
    if ch not in result:
        result += ch
print(result)
```
**S13 (choose the loop):** you need to print the **position** of every `"a"` in `"banana"`. Items loop or positions loop? Why? Write it.

**S14 (find the bug):**
```python
word = "level"
for ch in word:
    if word[ch] == "e":
        print("found")
```

### ✍️ Rewrite from memory
1. Day 04: **vowel counter** (count vowels in a word, any case)
2. Day 04: **palindrome check**
3. LeetCode 344: **Reverse String** in place (two pointers)
4. HackerRank: **Merge the Tools!** (try it with no peeking now)

### 💡 Better ways
approaches.md: Palindrome, Vowel counter, 344, Merge the Tools

---

## 📅 Sunday: `map`, parsing input, dictionaries (+ 📆 Sunday review)

### 📖 Reread
- [notes.md](../notes.md): "Reading many numbers from one line", Day 07 (dictionaries)
- [data-structures-guide.md](data-structures-guide.md) sections 1, 3 and 5
- [lessons/day07-dictionaries.md](day07-dictionaries.md): the tally-sheet part

### 🧠 Predict the output
```python
# M1  (pretend you typed: 4 5 6)
line = "4 5 6"
print(line.split())
# M2
print(map(int, line.split()))
# M3
print(list(map(int, line.split())))
# M4
print(list(map(str, [1, 2, 3])))
# M5
print(" ".join(map(str, [1, 2, 3])))
# M6
name, *rest = "Harsh 25 26".split()
print(name, rest)

d = {"a": 1, "b": 2}
# D1
print(d["a"], d.get("z"), d.get("z", 0))
# D2
for k in d:
    print(k, end=" ")
# D3
for k, v in d.items():
    print(k, v)
# D4
print(list(d.values()), len(d))
# D5
print("a" in d, 1 in d)
# D6
d["c"] = 3
d["a"] = 10
print(d)
# D7
counts = {}
for ch in "hello":
    counts[ch] = counts.get(ch, 0) + 1
print(counts)
```
**D8 (what happens?):** `print(d["z"])`

**D9 (find the bug):**
```python
counts = {}
for word in ["hi", "yo", "hi"]:
    counts[word] += 1
```

**D10 (choose):** you have `nums = [3, 8, 3]` and must print `3 8 3` on one line. Write it **two** ways.

### ✍️ Rewrite from memory
1. Day 07 Part 3: **letter counter + most common letter**
2. HackerRank: **Word Order**
3. HackerRank: **Finding the percentage** (many lines → a dictionary)
4. LeetCode 2161: **Partition by Pivot** (the tidier `for num in nums` version)

### 💡 Better ways
approaches.md: Word Order, Two Sum (the `seen` dict version), 2149, 2161

### 📆 Then: Sunday review
Claude gives a 10-question quiz on the whole week, logged in quiz-log.md.

---

<details>
<summary>✅ Answers (only after you've predicted!)</summary>

**Saturday**
- S1 `a a ana` · S2 `2 -1` · S3 `3 True False`
- S4 `banana`: string methods return a NEW string, so the result must be saved (`s = s.upper()`)
- S5 `['a', 'b', 'c']` · S6 `x-y-z` · S7 `a b c ` · S8 `0 1 2 `
- S9 `0 5` / `1 7` / `2 9` · S10 `1, 2, 3` · S11 `AB` · S12 `helo`
- S13 **positions loop**, because you need the position: `for i in range(len(s)):` / `if s[i] == "a": print(i)` → `1 3 5`
- S14 `ch` is already a **letter**, so `word[ch]` crashes ("string indices must be integers"). Use `if ch == "e":`

**Sunday**
- M1 `['4', '5', '6']` (still text) · M2 `<map object at 0x...>` (a recipe, not a list) · M3 `[4, 5, 6]`
- M4 `['1', '2', '3']` · M5 `1 2 3` · M6 `Harsh ['25', '26']`
- D1 `1 None 0` · D2 `a b ` (looping a dict gives **keys**) · D3 `a 1` / `b 2` · D4 `[1, 2] 2`
- D5 `True False` (`in` checks **keys**, not values) · D6 `{'a': 10, 'b': 2, 'c': 3}` (changing a key keeps its place)
- D7 `{'h': 1, 'e': 1, 'l': 2, 'o': 1}` · D8 **KeyError: 'z'**
- D9 KeyError on the first `"hi"`: the key doesn't exist yet. Use `counts[word] = counts.get(word, 0) + 1`
- D10 `print(" ".join(map(str, nums)))` or `for n in nums: print(n, end=" ")` (or `print(*nums)`)
</details>
