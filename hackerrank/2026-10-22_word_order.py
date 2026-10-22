# HackerRank: Word Order (Medium)
# https://www.hackerrank.com/challenges/word-order/problem
# 2026-10-22: COUNTING pattern (tally sheet). A dict keeps first-seen order.

n = int(input())
counts = {}

for i in range(n):
    word = input().strip()
    counts[word] = counts.get(word, 0) + 1
print(len(counts))
for letter, count in counts.items():
    print(count, end = " ")
