# LeetCode 42. Trapping Rain Water (Hard) - first Hard!
# https://leetcode.com/problems/trapping-rain-water/
# 2026-10-27: picture first (lessons/img/rain_water.png), then filled the blanks step by step,
# solution assembled from my answers and pasted. TODO: retype from memory + dig into it.
# Idea: water above bar i = min(tallest on the left, tallest on the right) - height[i]
# Patterns: BEST SO FAR twice (left -> right, then right -> left), [0] * n slots filled by position

class Solution:
    def trap(self, height: list[int]) -> int:
        n = len(height)

        left_max = [0] * n                  # pink row: tallest from the left
        best = 0
        for i in range(n):
            best = max(best, height[i])
            left_max[i] = best

        right_max = [0] * n                 # green row: tallest from the right
        best = 0
        for i in range(n - 1, -1, -1):
            best = max(best, height[i])
            right_max[i] = best

        total = 0                           # blue row: water above each bar
        for i in range(n):
            total += min(left_max[i], right_max[i]) - height[i]
        return total
