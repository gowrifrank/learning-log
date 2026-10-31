# LeetCode 9. Palindrome Number (Easy)
# https://leetcode.com/problems/palindrome-number/
# 2026-10-31: both versions Accepted (11513/11513).
# String way: fixed reverse(string) (NameError) -> string.reverse() (strings have no .reverse()) -> string[::-1],
# and true/false -> True/False.
# Bonus (follow-up, no string): own DIGIT PEEL + "calculator" rev = rev * 10 + digit, first try.
# Patterns: USE A BUILT-IN (slice), GUARD CLAUSE + DIGIT PEEL

class Solution:
    def isPalindrome(self, x: int) -> bool:
        string = str(x)
        if string == string[::-1]:
            return True
        else:
            return False


# Follow-up version (no string), also Accepted
class SolutionNoString:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        rev = 0
        real = x
        while x > 0:
            digit = x % 10
            rev = rev * 10 + digit
            x = x // 10
        if real == rev:
            return True
        else:
            return False
