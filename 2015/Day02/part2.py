# Part Two
# https://adventofcode.com/2015/day/3#part2

with open("input.txt") as file:
    text = file.read()

houses = set()

real_x, real_y = 0, 0
robo_x, robo_y = 0, 0
houses.add((0, 0))
real = True
for char in text:
    real = not real

    if real:
        if char == "^":
            real_y += 1
        elif char == "v":
            real_y -= 1
        elif char == ">":
            real_x += 1
        elif char == "<":
            real_x -= 1

        houses.add((real_x, real_y))
    else:
        if char == "^":
            robo_y += 1
        elif char == "v":
            robo_y -= 1
        elif char == ">":
            robo_x += 1
        elif char == "<":
            robo_x -= 1

        houses.add((robo_x, robo_y))

print(len(houses))
