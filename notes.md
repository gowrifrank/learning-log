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

## 🔥 HackerRank solved
- Python If-Else
- Arithmetic Operators
- Python: Division
- Loops
