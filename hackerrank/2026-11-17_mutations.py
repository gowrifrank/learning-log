# HackerRank: Mutations (Easy)
# https://www.hackerrank.com/challenges/python-mutations/problem
# 2026-11-17: strings are IMMUTABLE (can't change by position), lists are MUTABLE.
# So: string → list → change one item → "".join back to a string. (The problem text shows this way.)
# Fixed on the way: list[position] = ... (that's Python's built-in name "list") → stringlist[position]
# Pattern: CONVERT → CHANGE → CONVERT BACK (the same move as LeetCode 1528)

def mutate_string(string, position, character):
    stringlist = list(string)
    stringlist[position] = character
    stringlist = ''.join(stringlist)
    return stringlist

if __name__ == '__main__':
    s = input()
    i, c = input().split()
    s_new = mutate_string(s, int(i), c)
    print(s_new)
