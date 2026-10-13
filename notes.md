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

## 🔥 HackerRank solved
- Python If-Else
- Arithmetic Operators
- Python: Division
