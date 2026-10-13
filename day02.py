name = input("What is your name? ")
age = int(input("How old are you? "))

print(f"Hi {name}! In 10 years you'll be {age + 10}.")

if age >= 30:
    print("Experienced Human Detected")
else:
    print("Young Padawan Detected")

robot = input("What's your favourite robot? ")
year = int(input("Which year was it released? "))
robot_age = 2026 - year

print(f"{robot} is {robot_age} years old.")

if robot_age > 5:
    print("Classic!")
else:
    print("Brand new!")