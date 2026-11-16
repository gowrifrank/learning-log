# HackerRank: String Split and Join (Easy)
# https://www.hackerrank.com/challenges/python-string-split-and-join/problem
# 2026-11-16: own code from the STEP skeleton, right first time. split → join with "-".
# Tip: name the list "words" instead of reusing "line", so the name says what it holds.
# Pattern: SPLIT → JOIN (text → list → text, with new glue)

def split_and_join(line):
    # write your code here
    line = line.split(" ")
    line = "-".join(line)
    return line

if __name__ == '__main__':
    line = input()
    result = split_and_join(line)
    print(result)
