# LeetCode 1832. Check if the Sentence Is Pangram (Easy)
# https://leetcode.com/problems/check-if-the-sentence-is-pangram/
# 2026-11-08: own code after seeing the same shape on a vowels example. Flip the question:
# is every letter of the alphabet in the sentence? One missing -> False at once; loop finished -> True.
# Patterns: EARLY EXIT + FLAG-free "return after the loop"

class Solution:
    def checkIfPangram(self, sentence: str) -> bool:
        letters = "abcdefghijklmnopqrstuvwxyz"
        for letter in letters:
            if letter not in sentence:
                return False
        return True
