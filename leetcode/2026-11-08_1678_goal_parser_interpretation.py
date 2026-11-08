# LeetCode 1678. Goal Parser Interpretation (Easy)
# https://leetcode.com/problems/goal-parser-interpretation/
# 2026-11-08 (Diwali 🪔): own code after a .replace() refresher. Two swaps: "()" -> "o", then "(al)" -> "al".
# Remembered: strings can't change, so save the new string back (command = command.replace(...)).
# Pattern: USE A BUILT-IN (str.replace)

class Solution:
    def interpret(self, command: str) -> str:
        command = command.replace("()", "o")
        command = command.replace("(al)", "al")
        return command
