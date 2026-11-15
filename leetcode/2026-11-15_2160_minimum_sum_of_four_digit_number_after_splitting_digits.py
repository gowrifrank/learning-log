# LeetCode 2160. Minimum Sum of Four Digit Number After Splitting Digits (Easy)
# https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/
# 2026-11-15: last vacation day. Code given by Claude; plan is to relearn it after 15 Nov.
# 🔁 Redo it solo later (no peeking): see the backlog in progress.md.
# Patterns: SORT FIRST + greedy (the smallest digits go in the tens places)

class Solution:
    def minimumSum(self, num: int) -> int:
        d = sorted(str(num))                    # 2932 → ['2', '2', '3', '9']
        new1 = int(d[0] + d[2])                 # '2' + '3' = '23' → 23
        new2 = int(d[1] + d[3])                 # '2' + '9' = '29' → 29
        return new1 + new2                      # 23 + 29 = 52
