# LeetCode 151. Reverse Words in a String (Medium)
# https://leetcode.com/problems/reverse-words-in-a-string/
# 2026-11-17: own code, first Medium after the vacation. split() (no argument) drops ALL extra spaces.
# Fixed: newstr[len(newstr):-1] gave [] (start 4, stop -1, walking FORWARD) → the direction goes in the
# THIRD slot, the step: newstr[::-1].
# Tip: newstr holds a LIST of words, so "words" would be a clearer name.
# Patterns: SPLIT → REVERSE → JOIN

class Solution:
    def reverseWords(self, s: str) -> str:
        newstr = s.split()
        strrev = newstr[::-1]
        return " ".join(strrev)
