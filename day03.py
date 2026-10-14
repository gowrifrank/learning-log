# Day 03
# Part 01 : Times Table

num = int(input("Enter the number whose table needs to be viewed: "))

for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

# Part 02: Even Numbers from 2 to 20

print("--- Even numbers - Method 1 ---")
for i in range(2, 21, 2):
    print(i)

print("--- Even numbers - Method 2 ---")
for i in range(2, 21):
    if i % 2 == 0:
        print(i)

# Part 03: Robotic Countdown using While

print("--- Robotic Countdown ---")
count = 5
while count > 0:
    print(count)
    count -= 1
print("Optimus activated 🤖")

# BONUS: Add all numbers from 0 to 100 and print them

total = 0
for i in range(1, 101):
    total += i
print(total)  