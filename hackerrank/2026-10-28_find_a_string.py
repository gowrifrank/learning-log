# HackerRank: Find a String (Easy)
# https://www.hackerrank.com/challenges/find-a-string/problem
# 2026-10-28: own logic! A sliding find(): search only inside the window [i, str_end), and move the
# window's end along with i. Fixed: find() returns a POSITION or -1 (not True/"True").
# Pattern: SLIDING WINDOW (check every start position, overlaps included)

def count_substring(string, sub_string):
    str_count = 0
    str_end = len(sub_string)
    for i in range(len(string)):
        pos = string.find(sub_string, i, str_end)   # search only string[i:str_end]
        if pos != -1:                                # -1 = not found
            str_count += 1
        str_end += 1                                 # slide the window's end with i
    return str_count

if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()

    count = count_substring(string, sub_string)
    print(count)
