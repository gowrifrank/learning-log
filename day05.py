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

