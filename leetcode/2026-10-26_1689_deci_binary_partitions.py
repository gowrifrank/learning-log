# LeetCode 1689. Partitioning Into Minimum Number Of Deci-Binary Numbers (Medium)
# https://leetcode.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/
# 2026-10-26: own greedy idea on paper (biggest deci-binary that fits, repeat) -> spotted that
# each number takes at most 1 from every column, so the BIGGEST DIGIT is the answer.
# Pattern: BEST SO FAR over the characters of a string

class Solution:
    def minPartitions(self, n: str) -> int:
        best = 0
        for ch in n:
            if int(ch) > best:
                best = int(ch)
        return best
