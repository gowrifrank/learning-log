# LeetCode 2011. Final Value of Variable After Performing Operations (Easy)
# https://leetcode.com/problems/final-value-of-variable-after-performing-operations/
# 2026-11-05: own code, first try (0 ms). Start at 0, loop over the instructions,
# +1 for the two "plus" forms, -1 for everything else.
# Pattern: ACCUMULATOR

class Solution:
    def finalValueAfterOperations(self, operations: list[str]) -> int:
        x = 0
        for operation in operations:
            if operation == "++X" or operation == "X++":
                x += 1
            else:
                x -= 1
        return x
