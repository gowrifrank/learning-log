# LeetCode 1528. Shuffle String (Easy)
# https://leetcode.com/problems/shuffle-string/
# 2026-11-13: busy vacation evening. Code given by Claude; plan is to relearn it after 15 Nov.
# 🔁 Redo it solo later (no peeking): see the backlog in progress.md.
# Patterns: PRE-SIZED LIST + write each item straight to its slot, then join

class Solution:
    def restoreString(self, s: str, indices: list[int]) -> str:
        result = [""] * len(s)              # empty slots, one per letter
        for i in range(len(s)):
            result[indices[i]] = s[i]       # letter i goes to slot indices[i]
        return "".join(result)              # list of letters → text
