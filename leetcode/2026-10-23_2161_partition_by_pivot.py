# LeetCode 2161. Partition Array According to Given Pivot (Medium)
# https://leetcode.com/problems/partition-array-according-to-given-pivot/
# 2026-10-23: FILTER into 3 lists, then join them end to end with +

class Solution:
    def pivotArray(self, nums: list[int], pivot: int) -> list[int]:
        less = []
        equals = []
        more = []
        for i in range(len(nums)):
            if nums[i] < pivot:
                less.append(nums[i])
            if nums[i] == pivot:
                equals.append(nums[i])
            if nums[i] > pivot:
                more.append(nums[i])
        return less + equals + more
