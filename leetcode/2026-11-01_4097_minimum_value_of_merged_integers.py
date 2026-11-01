# LeetCode 4097. Minimum Value of Merged Integers (Easy)
# https://leetcode.com/problems/minimum-value-of-merged-integers/
# 2026-11-01: Weekly Contest 526, Q1. My FIRST contest! Solved solo, no AI, Accepted first try (999/999, 1 ms) at 08:26.
# Idea: step through the list in pairs (range with step 2), glue each pair as text, turn it back into a number,
# collect them all, return the smallest.
# Patterns: PAIRS (range(0, n, 2)), ACCUMULATOR list + USE A BUILT-IN (min)

class Solution:
    def minMergedInteger(self, nums: list[int]) -> int:
        values = []
        for i in range(0, len(nums), 2):
            val = int(str(nums[i]) + str(nums[i + 1]))
            values.append(val)
        return min(values)
