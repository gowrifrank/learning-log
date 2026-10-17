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

# Part 03 : Count Vowels

def count_vowels(text):
    total = 0
    for ch in text.lower():
        if ch in "aeiou":
            total += 1
    return total
ip_word = input("Enter the word to check the vowel count: ")
result = count_vowels(ip_word)
print(f"The total number of vowels : {result}")

# Part 04 : Second Highest Score

def second_highest(scores):
    scores.sort()
    second_best = max(scores)
    for i in range(len(scores) - 1, 0, -1):
        if scores[i] > scores[i-1]:
            second_best = scores[i-1]
            break
    return second_best

inp_scores = [72, 95, 88, 61, 79]
sec_high_score_res = second_highest(inp_scores)
print(f"The Second-Highest score is: {sec_high_score_res}")

