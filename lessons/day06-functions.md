# 📘 Day 06: Functions 🧩
A **function** is a named, reusable block of code. You've been *using* them all along (`print()`, `len()`, `max()`). Now you make your own.

## 1. Define and call
```python
def greet():                  # def = define a function
    print("Hello, Gowri!")

greet()                       # call it (and reuse it as often as you like)
```

## 2. Parameters = input
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Optimus")              # Hello, Optimus!
```

## 3. `return` = output ⭐
```python
def square(n):
    return n * n              # hands the answer BACK to the caller

result = square(5)            # 25
print(square(3) + square(4))  # 25
```

### ⚠️ `print` vs `return`: the #1 trap
```python
def add_print(a, b):
    print(a + b)              # only shows it on screen

def add_return(a, b):
    return a + b              # gives the value back so you can use it

x = add_print(2, 3)           # shows 5, but x = None 😱 (just like .sort()!)
y = add_return(2, 3)          # y = 5 ✅
```

## 4. `return` exits immediately
```python
def is_even(n):
    if n % 2 == 0:
        return True           # stops here
    return False              # only reached if the if was False

# shorter: return n % 2 == 0  (the comparison already IS True or False)
```

## 5. Defaults
```python
def power(base, exp=2):
    return base ** exp

power(3)      # 9  (exp defaults to 2)
power(2, 5)   # 32
```

## 6. Inside stays inside
```python
def make_total():
    total = 100
make_total()
print(total)   # ❌ NameError: use return to get values out
```

---

## ✍️ Exercise: `day06.py`
Turn your old code into reusable tools 🧰
1. `is_even(n)` → True/False. Test with 4 and 7.
2. `is_palindrome(word)` → True/False, ignoring case (reuse Day 04)
3. `count_vowels(text)` → number of vowels (reuse Day 04)
4. `second_highest(scores)` → handles duplicates (reuse Day 05 / Runner-Up)
5. `average(numbers)` → the average of a list

Call each one and print the result:
```python
print(is_palindrome("Racecar"))           # True
print(second_highest([95, 95, 88, 61]))   # 88
```
**Bonus:** `grade(score)` → `"A"` for 90 or more (90 counts!), `"B"` for 75–89, `"C"` for 50–74, below 50 `"F"`. Use early `return`s, with no `elif` needed!

---

## 🔥 HackerRank: [Write a function](https://www.hackerrank.com/challenges/write-a-function/problem)
Return `True` if a year is a **leap year**:
- divisible by **4** → leap...
- **unless** divisible by **100** → not leap...
- **unless** also divisible by **400** → leap again!

Test values: 2000 ✅, 1900 ❌, 2024 ✅, 2023 ❌

**Hints:**
- `year % 4 == 0` checks divisibility
- Use early `return` and check the **most specific rule first** (400 → 100 → 4)
- Keep HackerRank's `def is_leap(year):` and fill in the logic
