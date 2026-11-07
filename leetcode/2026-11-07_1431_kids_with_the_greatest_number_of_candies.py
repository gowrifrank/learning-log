# LeetCode 1431. Kids With the Greatest Number of Candies (Easy)
# https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/
# 2026-11-07: own code, first try (0 ms). For each kid: with all the extra candies, do they reach the biggest pile?
# Improve next time: max(candies) is recalculated in EVERY round; work it out once before the loop.
# Patterns: BUILD A LIST + USE A BUILT-IN (max)

class Solution:
    def kidsWithCandies(self, candies: list[int], extraCandies: int) -> list[bool]:
        result = []
        for candy in candies:
            if candy + extraCandies >= max(candies):
                result.append(True)
            else:
                result.append(False)
        return result
