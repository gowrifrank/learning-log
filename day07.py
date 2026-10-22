# Day 07
# Part 01 : Robot Profile

def robot_print(robot_inp):
    print("Robot Details: ")
    #print(robot_inp.items())
    for key, value in robot_inp.items():
        print(f"{key}: {value}")

def update_robot(robot):
    robot_print(robot)

    robot["price"] = 20000
    robot["year"] = "2024"
    del robot["height"]

    robot_print(robot)

robot_dic = {
    "name": "Optimus",
    "maker": "Tesla",
    "year": "2022",
    "height": "1.51 m"
}
update_robot(robot_dic)

# Part 02 : Phonebook

contact = {
    "gowri": "9500262191",
    "freddy": "7708793409",
    "pons": "8807182853",
    "prax": "9500799001"
}
name = input("Whose number? ")
print(contact.get(name, "Not Found"))

# Part 03 : Letter Counter

word = input("Word: ").lower()
counts = {}
best_letter = None
best_count = 0
for ch in word:
    counts[ch] = counts.get(ch, 0) + 1
print(counts)
for letter, count in counts.items():
    if count > best_count:
        best_letter = letter
        best_count = count
print(f"Most common: {best_letter} ({best_count} times)")

# Part 04 : Grade Book

def grades(score):
    if score >= 90:
        return "A"
    if 89 >= score >= 75:
        return "B"
    if score >= 50:
        return "C"
    return "F"

scores = {
    "Gowri": 92,
    "Atlas": 74,
    "ASIMO": 58,
    "Spot": 81
}
grade = None
for name, score in scores.items():
    grade = grades(score)
    print(f"{name}: {grade}")

# BONUS : Two Sum

def two_sum(nums, target):
    count = 0
    for i in range(len(nums)):
        if nums[i] <= target:
            count += 1
    for j in range(count -1, 0, -1):
        for i in range(0, j):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None

nums = list(map(int, input("Numbers in Increasing Order: ").split()))
target = int(input("Target: "))
print(two_sum(nums, target))


    