# Part One
# https://adventofcode.com/2025/day/1

with open("input.txt") as file:
    text = file.read()


def rotate(current, rotation):
    current += rotation

    while current > 99:
        current -= 100
    while current < 0:
        current += 100

    return current


text = text.replace("L", "-")
text = text.replace("R", "")
rotations = text.split("\n")
rotations = map(int, rotations)

position = 50
zeros = 0
for rotation in rotations:
    position = rotate(position, rotation)
    if position == 0:
        zeros += 1

print(zeros)
