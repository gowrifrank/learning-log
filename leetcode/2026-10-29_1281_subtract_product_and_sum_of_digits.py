# LeetCode 1281. Subtract the Product and Sum of Digits of an Integer (Easy)
# https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/
# 2026-10-29: own string-loop idea. Fixed list{n} (SyntaxError) -> list("n") (the LETTER n,
# ValueError) -> str(n) (the variable turned into text), and int(number) for each character.
# Pattern: ACCUMULATOR x2 (product starts at 1, sum starts at 0)

class Solution:
    def subtractProductAndSum(self, n: int) -> int:
        num_list = str(n)
        prod = 1
        add = 0
        for number in num_list:
            prod = prod * int(number)
            add += int(number)
        result = prod - add
        return result
