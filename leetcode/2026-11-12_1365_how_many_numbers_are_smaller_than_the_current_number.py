# LeetCode 1365. How Many Numbers Are Smaller Than the Current Number (Easy)
# https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/
# 2026-11-12: busy vacation evening. Code given by Claude; plan is to relearn it after 15 Nov.
# 🔁 Redo it solo later (no peeking): see the backlog in progress.md.
# Patterns: loop inside a loop (compare each number with every number) + COUNTING

class Solution:
    def smallerNumbersThanCurrent(self, nums: list[int]) -> list[int]:
        result = []
        for x in nums:               # pick one number
            count = 0
            for y in nums:           # compare it with every number
                if y < x:
                    count += 1       # COUNTING: one more smaller number
            result.append(count)
        return result
