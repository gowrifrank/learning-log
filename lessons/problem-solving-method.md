# 🧘 How to Solve a Problem Without Panicking
> "I can solve the logic, but I can't write the code" is **normal**. Logic and code are two different skills. This method connects them. **Never write the whole program at once.**

## The 6-step method
### 1. Solve the sample by hand ✏️
Read the sample input and work out the answer on paper **without code**. If you can't do it by hand, you can't code it yet.

### 2. Write the steps as comments 📝
Turn your hand-solution into short English steps, as `#` comments in the editor:
```python
# STEP 1: read all students into a list of [name, score]
# STEP 2: make a sorted list of just the scores
# STEP 3: find the second-lowest score
# STEP 4: collect the names with that score
# STEP 5: sort the names and print each one
```
Now the big scary problem is **5 small problems**.

### 3. For each step, ask "what am I holding?" 🔍
Write the **shape** of the data next to each step:
```python
# students = [["Harry", 37.21], ["Tina", 37.2], ...]   (list of lists)
# scores   = [37.2, 37.21, 37.21, 39.0, 41.0]          (list of numbers)
# second   = 37.21                                       (one number)
# names    = ["Berry", "Harry"]                          (list of strings)
```

### 4. Code ONE step, then `print()` and run ▶️
Write only Step 1, add `print(students)`, click **Run**. Does the output match the shape you wrote? ✅ Then move on. ❌ Fix just this step.
**Small steps = small errors = no panic.**

### 5. Translate English → Python with the "phrasebook" 📖
| When I want to... | Python |
|---|---|
| start an empty list | `x = []` |
| add something to a list | `x.append(thing)` |
| go through every item | `for item in x:` |
| keep only some items | `if condition:` inside the loop, then `append` |
| sort a list | `x.sort()` or `sorted(x)` |
| get the first / last | `x[0]` / `x[-1]` |
| inside a pair `[name, score]` | `pair[0]` = name, `pair[1]` = score |
| stop at the first match | `break` |
| count things | `counts[k] = counts.get(k, 0) + 1` |
| print each item on its own line | `for item in x: print(item)` |

### 6. Clean up and submit 🧹
Remove the debug `print()`s, test the sample once more, and submit. If it fails, look at the failing input and ask: "what's different about it?"

## 🚑 When panic hits
- Stop typing. Breathe. **Go back to step 1** (by hand).
- Delete nothing. Comment the broken code out with `#` and start the current step again.
- A red squiggle = **one** small problem. Fix the **first** one only, then re-run.
- `return` only works inside `def`. On HackerRank's main code, use `print`.

## Common syntax traps from my journal
- Filling an empty list with `x[0] = ...` → use `x.append(...)`
- `x.sorted()` ❌ → `sorted(x)` or `x.sort()`
- `for item in range(len(x))` gives **positions**, so use `x[item]` to get the value
- `return` outside a function ❌ → `print()`
