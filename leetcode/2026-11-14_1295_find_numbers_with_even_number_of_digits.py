# LeetCode 1295. Find Numbers with Even Number of Digits (Easy)
# https://leetcode.com/problems/find-numbers-with-even-number-of-digits/
# 2026-11-14: vacation morning. Code given by Claude; plan is to relearn it after 15 Nov.
# 🔁 Redo it solo later (no peeking): see the backlog in progress.md.
# Patterns: COUNTING + number → text with str() to count digits

class Solution:
    def findNumbers(self, nums: list[int]) -> int:
        count = 0
        for num in nums:
            if len(str(num)) % 2 == 0:      # str(7896) = "7896" → 4 digits → even
                count += 1
        return count
