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
    "amy": "9000000001",
    "ben": "9000000002",
    "cara": "9000000003",
    "dev": "9000000004"
}
name = input("Whose number? ")
print(contact.get(name, "Not Found"))