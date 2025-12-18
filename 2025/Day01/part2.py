# Part Two
# https://adventofcode.com/2025/day/1#part2

with open("input.txt") as file:
    text = file.read()


def rotate(current, rotation):
    zeros = abs(rotation) // 100
    remainder = abs(rotation) % 100 * (-1 if rotation < 0 else 1)

    original = current
    current += remainder

    if original != 0 and (current <= 0 or current >= 100):
            zeros += 1

    current %= 100

    return current, zeros


text = text.replace("L", "-")
text = text.replace("R", "")
rotations = text.split("\n")
rotations = map(int, rotations)

position = 50
zeros = 0
for rotation in rotations:
    position, rotation_zeros = rotate(position, rotation)
    zeros += rotation_zeros

print(zeros)
