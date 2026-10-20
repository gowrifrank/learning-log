# LeetCode 1108: Defanging an IP Address (Easy)
# Solved: 2026-10-20 · Accepted 62/62
# Pattern: string ACCUMULATOR (build a new string letter by letter)

class Solution:
    def defangIPaddr(self, address: str) -> str:
        output = ""
        for ch in address:
            if ch == ".":
                output = output + "[.]"
            else:
                output = output + ch
        return output
