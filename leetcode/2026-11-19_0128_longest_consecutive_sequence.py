# LeetCode 128. Longest Consecutive Sequence (Medium)
# https://leetcode.com/problems/longest-consecutive-sequence/
# 2026-11-19: off day → final code given by Claude, built on MY start: set(nums) + a counting walk
# (count += 1, currentnumber += 1). 🔁 Redo solo later.
# My first try only counted the run starting at min(nums) → wrong for [1, 2, 10, 11, 12] (gave 2, answer 3),
# crashed on [] (min of an empty list), and used print instead of return.
# Also fixed: min.nums → AttributeError → min(nums) (functions go AROUND, a dot means "a tool of this thing")
# 🔑 Start rule: if num - 1 is NOT in the set, nobody stands in front of num → it STARTS a run.
# Only starts walk up, so each run is counted once → fast (O(n), no sorting).
# A set has NO order: small numbers only LOOK sorted. sorted(set(x)) if order is needed.
# Patterns: SET FOR FAST "in" + BEST SO FAR + a while walk

class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        newset = set(nums)
        best = 0
        for num in newset:
            if num - 1 not in newset:
                currentnumber = num
                count = 0
                while currentnumber in newset:
                    count += 1
                    currentnumber += 1
                if count > best:
                    best = count
        return best
