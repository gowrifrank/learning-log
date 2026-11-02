# LeetCode 58. Length of Last Word (Easy)
# https://leetcode.com/problems/length-of-last-word/
# 2026-11-02: own idea (split → last word → len). Fixed two slips:
#   print(...) -> return ... (LeetCode reads the RETURN value; print gave null)
#   array.append(s.split()) -> array = s.split() (append put the whole list inside a list: [['Hello', 'World']])
# Patterns: USE A BUILT-IN (split + [-1])

class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        array = []
        strlen = ""
        array = s.split()       # words only, all spaces thrown away
        strlen = array[-1]      # the last word
        return len(strlen)
