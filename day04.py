# Day 04
# Part 01 : Name Card

name = input("Enter your full name: ")
print(f"Your Name in UPPERCASE: {name.upper()}")
print(f"Your Name in lowercase: {name.lower()}")
print(f"The length of your name is: {len(name)} Characters")
print(f"The First letter of your name is: {name[0]}")

# Part 02 : Reverse

word = input("Enter a word to print it sdrawkcab: ")
print(f"The sdrawkcab of {word} is {word[::-1]} written backwards")

# Part 03 : Palindrome Checker

inp = input("Enter the word to check for a palindrome: ")
inp = inp.lower()

if inp == inp[::-1]:
    print(f"{inp} is a palindrome")
else:
    print(f"{inp} is NOT a palindrome")

# Part 03-01 : Palindrome Checker

n = -1
count = 0
for i in range(len(inp)):    # i = positions 0, 1, 2, ...
    if inp[i] != inp[n]:     # compare letter from the front with letter from the back
        count += 1           # count mismatches
    n -= 1                   # move the back pointer one step left, every round
if count == 0:
    print(f"{inp} is a palindrome")
else:
    print(f"{inp} is NOT a palindrome")

# Part 04 : Vowel Counter

ip_word = input("Enter the word to check the vowel count: ")
ip_word = inp.lower()
total = 0
for ch in ip_word:
    if ch in "aeiou":
        total += 1
print(f"The total number of vowels in the entered word is: {total}")