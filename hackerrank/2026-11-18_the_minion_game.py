# HackerRank: The Minion Game (Medium)
# https://www.hackerrank.com/challenges/the-minion-game/problem
# 2026-11-18: own code (pending since 27 Oct!). The first letter of a piece decides who scores:
# vowel → Kevin, consonant → Stuart. Shortcut: pieces starting at position i = letters left = len - i,
# so no piece is ever built (a 1,000,000-letter word runs in about 0.1 s).
# My own idea: "multiplier" starts at len(string) and counts down by 1, instead of len(string) - i.
# Fixed on the way:
#   - array.append(string) put the WHOLE word in as ONE item → just use string[i]
#   - array.lower() → AttributeError (lists have no .lower), and the word is always uppercase anyway
#   - x != 'a' or 'e' or ... is ALWAYS True ('e' on its own counts as True) → string[i] not in "AEIOU"
# Patterns: COUNT EACH SPOT'S SHARE + ACCUMULATOR (two scores)

def minion_game(string):
    Stuart = 0
    Kevin = 0
    multiplier = len(string)
    for i in range(0,len(string)):
        if string[i] not in "AEIOU":
            Stuart += multiplier
        else:
            Kevin += multiplier
        multiplier -= 1
    if Stuart > Kevin:
        print(f"Stuart {Stuart}")
    elif Stuart < Kevin:
        print(f"Kevin {Kevin}")
    else:
        print("Draw")

if __name__ == '__main__':
    s = input()
    minion_game(s)
