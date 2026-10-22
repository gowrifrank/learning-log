# LeetCode 2149. Rearrange Array Elements by Sign (Medium)
# https://leetcode.com/problems/rearrange-array-elements-by-sign/
# 2026-10-22: first Medium! Patterns: FILTER (twice) + BUILD A LIST

class Solution:
    def rearrangeArray(self, nums: list[int]) -> list[int]:
        # STEP 1: make two empty lists: positives and negatives
        # STEP 2: loop over nums → put each number in the right list
        # STEP 3: make an empty result list
        # STEP 4: loop over POSITIONS 0, 1, 2 … up to the length of positives
        # STEP 5: add positives[i] to result, then negatives[i]
        # STEP 6: return result
        positives = []
        negatives = []
        result = []
        for i in range(len(nums)):
            if nums[i] >= 0:
                positives.append(nums[i])
            elif nums[i] < 0:
                negatives.append(nums[i])

        for k in range(len(positives)):
            result.append(positives[k])
            result.append(negatives[k])
        return result
