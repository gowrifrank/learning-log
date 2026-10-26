# HackerRank: Piling Up! (Medium)
# https://www.hackerrank.com/challenges/piling-up/problem
# 2026-10-26: own idea (pop from the ends, take the bigger end); fixed pop(value) -> pop(position),
# added the "top of the pile" check and an ok flag after a walkthrough. Earned the 4th Python star.
# Patterns: take from BOTH ENDS (greedy: bigger end first), BEST SO FAR in reverse (top only shrinks), FLAG

T = int(input())
for i in range(T):
    blocksize = int(input())
    blocks = list(map(int, input().split()))
    top = float("inf")               # empty pile: "infinitely big", so any first cube fits
    ok = True                        # innocent until proven guilty
    for j in range(blocksize):
        if blocks[0] >= blocks[-1]:  # left end is bigger (or equal)
            picked = blocks.pop(0)   #   take from the left
        else:
            picked = blocks.pop()    #   take from the right
        if picked > top:             # bigger than what's below? it can't go there
            ok = False
            break                    # no point checking the rest
        top = picked                 # it fits, so it's the new top of the pile
    print("Yes" if ok else "No")     # ONE answer per test case
