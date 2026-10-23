# HackerRank: Merge the Tools! (Medium)
# https://www.hackerrank.com/challenges/merge-the-tools/problem
# 2026-10-23: own window idea first, then typed this version after a walkthrough.
# Patterns: jump through a string with range(0, n, k) + slicing, BUILD A STRING with a "not in" check

def merge_the_tools(string, k):
    for start in range(0, len(string), k):    # start of each piece: 0, k, 2k ...
        piece = string[start : start + k]      # cut k letters
        result = ""                            # fresh for EVERY piece
        for ch in piece:
            if ch not in result:               # kept already? skip it
                result += ch
        print(result)

if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)
