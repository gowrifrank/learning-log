# LeetCode 1470. Shuffle the Array (Easy)
# https://leetcode.com/problems/shuffle-the-array/
# 2026-11-05: own code. Each y sits n positions after its x, so loop n rounds and add 2 numbers per round.
# Fixed: range(0, j * 2) ran 6 rounds -> nums[i + j] asked for nums[6] -> IndexError. Only n rounds are needed.
# Also dropped j = int(len(nums) / 2): LeetCode already gives n.
# Patterns: PAIRS (x at i, partner y at i + n) + BUILD A LIST

class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        finallist = []
        for i in range(0, n):
            finallist.append(nums[i])
            finallist.append(nums[n + i])
        return finallist
