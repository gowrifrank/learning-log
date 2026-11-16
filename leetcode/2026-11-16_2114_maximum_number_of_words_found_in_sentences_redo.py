# LeetCode 2114. Maximum Number of Words Found in Sentences (Easy): SOLO REDO ✅
# https://leetcode.com/problems/maximum-number-of-words-found-in-sentences/
# 2026-11-16: first problem back from vacation, written by me (the 10 Nov version was given code).
# My idea: words = spaces + 1. Fixed two slips on the way:
#   range(len(sentences)) gave positions (AttributeError: 'int' object has no attribute 'count')
#   count(" ") counts spaces, so the answer was one short
# Bonus: the "+ 1" goes once on the return, because adding 1 to every count doesn't change which is biggest.
# Patterns: BEST SO FAR + count spaces

class Solution:
    def mostWordsFound(self, sentences: list[str]) -> int:
        best = 0
        for sentence in sentences:
            count = sentence.count(" ")
            if count > best:
                best = count
        return best + 1
