# LeetCode 1920. Build Array from Permutation (Easy)
# https://leetcode.com/problems/build-array-from-permutation/
# 2026-10-28: first try, no hints. Positions loop + append; nums[nums[i]] read inside-out.
# Pattern: BUILD A LIST (value at one position = the next position to look up)

class Solution:
    def buildArray(self, nums: list[int]) -> list[int]:
        ans = []
        for i in range (len(nums)):
            ans.append(nums[nums[i]])
        return ans
