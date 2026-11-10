# LeetCode 2114. Maximum Number of Words Found in Sentences (Easy)
# https://leetcode.com/problems/maximum-number-of-words-found-in-sentences/
# 2026-11-10: tired vacation evening. Code given by Claude from my STEP skeleton; I typed it in and submitted.
# 🔁 Redo it solo later (no peeking): see the backlog in progress.md.
# Patterns: BEST SO FAR + split() to count words

class Solution:
    def mostWordsFound(self, sentences: list[str]) -> int:
        best = 0                              # STEP 1: nothing seen yet
        for sentence in sentences:            # STEP 2: one sentence at a time
            count = len(sentence.split())     # STEP 3: words in THIS sentence
            if count > best:                  # STEP 4: beats the best so far?
                best = count
        return best                           # STEP 5: after the loop
