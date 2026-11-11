# LeetCode 1816. Truncate Sentence (Easy)
# https://leetcode.com/problems/truncate-sentence/
# 2026-11-11: busy vacation evening. Code given by Claude from my STEP skeleton.
# 🔁 Redo it solo later (no peeking): see the backlog in progress.md.
# Patterns: split → slice → join (text → list → text)

class Solution:
    def truncateSentence(self, s: str, k: int) -> str:
        words = s.split()            # STEP 1: text → list of words
        first_k = words[:k]          # STEP 2: keep the first k words
        return " ".join(first_k)     # STEP 3: list → text, glued with spaces
