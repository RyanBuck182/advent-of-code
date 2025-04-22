# Part One
# https://adventofcode.com/2015/day/2

with open("input.txt") as file:
    text = file.read()

boxes = text.split('\n')

total_feet = 0
for box in boxes:
    l, w, h = map(int, box.split('x'))
    sides = [l*w, w*h, h*l]
    smallest_side = min(*sides)

    total_feet += 2 * sum(sides) + smallest_side

print(total_feet)
