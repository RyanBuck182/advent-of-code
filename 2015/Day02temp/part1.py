# Part One
# https://adventofcode.com/2015/day/3

with open("input.txt") as file:
    text = file.read()

houses = set()

x, y = 0, 0
houses.add((0, 0))
for char in text:
    if char == "^":
        y += 1
    elif char == "v":
        y -= 1
    elif char == ">":
        x += 1
    elif char == "<":
        x -= 1

    houses.add((x, y))

print(len(houses))
