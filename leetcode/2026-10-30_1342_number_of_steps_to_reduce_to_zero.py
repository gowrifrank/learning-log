# LeetCode 1342. Number of Steps to Reduce a Number to Zero (Easy)
# https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/
# 2026-10-30: own idea: loop while num > 1, then +1 for the last step (1 -> 0).
# Fixed: num = 0 returned 1 (added a GUARD CLAUSE), and num / 2 -> num // 2 (keeps num an int).
# Pattern: GUARD CLAUSE + COUNTER in a while loop

class Solution:
    def numberOfSteps(self, num: int) -> int:
        steps = 0
        if num == 0: return steps
        while num > 1:
            if num % 2 == 0:
                steps += 1
                num = num // 2
            elif num % 2 != 0:
                steps +=1
                num -= 1
        steps += 1
        return steps
