# Day 05
# Part 01 : Robot Collection

robots = ["Atlas", "ASIMO", "Optimus"]
robots.append("Unitree")
robots.insert(0, "Nvidia")
print("Robots before removal: ")

for robot in robots:
    print(robot)
robots.remove(robots[1])
robots.pop(2)

print("Robots after removal: ")

for robot in robots:
    print(robot)

# Part 02 : Score Stats

scores = [72, 95, 88, 61, 79]
print(f"The SUM of the scores is: {sum(scores)}")
print(f"The HIGHEST of the scores is: {max(scores)}")
print(f"The LOWEST of the scores is: {min(scores)}")
print(f"The AVERAGE of the scores is: {sum(scores)/len(scores)}")

# Part 03 : Even Filter

numbers = [3, 8, 15, 22, 7, 4]
even = []

for num in numbers:
    if num%2 == 0:
        even.append(num)
print(f"Even Numbers: {even}")

# Part 04 : Word Counter

sentence = input("Enter the sentence to be evaluated: ")
words = sentence.split()
print(f"The number of words in the sentence are: {len(words)}")

# BONUS : Second - Highest Score

scores = [72, 95, 88, 61, 79]
scores.sort()
second_best = max(scores)
for i in range(len(scores) - 1, 0, -1):
    if scores[i] > scores[i-1]:
        second_best = scores[i-1]
        break
print(f"The Second-Highest score is: {second_best}")
# print(f"The Second-Highest score is: {scores[len(scores)-2]}") #It won't work for a list with 2 or more max identical numbers.
