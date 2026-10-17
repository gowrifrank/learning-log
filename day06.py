# Day 06
# Part 01 : Is Even

def is_even(n):
    if n % 2 == 0:
        return True
    return False

x = int(input("Enter a number: "))
op = is_even(x)
print(f"Is the entered number Even? : {op}")


