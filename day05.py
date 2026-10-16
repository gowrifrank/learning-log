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

