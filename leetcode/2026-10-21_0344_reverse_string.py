# LeetCode 344: Reverse String (Easy)
# Solved: 2026-10-21 · Accepted
# Pattern: TWO POINTERS, swapping in place

class Solution:
    def reverseString(self, s: list[str]) -> None:
        first = 0
        last = len(s) - 1
        while (first < last):
            swap = s[first]
            s[first] = s[last]
            s[last] = swap
            first += 1
            last -= 1
