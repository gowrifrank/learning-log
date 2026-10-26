# LeetCode 412. Fizz Buzz (Easy)
# https://leetcode.com/problems/fizz-buzz/
# 2026-10-25: BUILD A LIST with exclusive conditions (order-independent)

class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        result = []
        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 != 0:
                result.append("Fizz")
            elif i % 3 != 0 and i % 5 == 0:
                result.append("Buzz")
            elif i % 3 == 0 and i % 5 == 0:
                result.append("FizzBuzz")
            else:
                result.append(str(i))
        return result
