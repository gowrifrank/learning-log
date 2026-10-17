# Day 06
# Part 01 : Is Even

def is_even(n):
    if n % 2 == 0:
        return True
    return False

x = int(input("Enter a number: "))
op = is_even(x)
print(f"Is the entered number Even? : {op}")


# Part 02 : Palindrome Checker

def is_palindrome(word):
    if word.lower() == word[::-1].lower():
        return True
    return False

inp_wd = input("Enter the word to check for a palindrome: ")
pal = is_palindrome(inp_wd)
print(f"Is the entered word a Palindrome? : {pal}")

