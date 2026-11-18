# LeetCode 1561. Maximum Number of Coins You Can Get (Medium)
# https://leetcode.com/problems/maximum-number-of-coins-you-can-get/
# 2026-11-18: own code, after finding the pattern on paper. 116/116, 74 ms.
# Key idea: *I* choose the groups of 3. Bob always takes the smallest → give him the n smallest piles.
# Alice always takes the biggest → pair her pile with the one just below it, so I get that one.
# Sorted [1 2 3 | 4 5 6 7 8 9]: Bob 1 2 3, then I take every SECOND pile from position n: 4, 6, 8 = 18.
# Fixed on the way:
#   - sorted(piles) on its own line did nothing (it returns a NEW list) → piles.sort() sorts in place
#   - indicator += 1 took 4 5 6 (= 15) → += 2 skips Alice's piles (= 18)
# Patterns: GREEDY (best choice at each step) + SORT FIRST + ACCUMULATOR + a jump of 2 (like PAIRS)

class Solution:
    def maxCoins(self, piles: list[int]) -> int:
        myself = 0
        indicator = int(len(piles)/3)
        rangef = indicator
        count = 0
        piles.sort()
        while count < rangef:
            myself += piles[indicator]
            count += 1
            indicator += 2
        return myself
