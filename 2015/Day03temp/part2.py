# Part Two
# https://adventofcode.com/2015/day/2#part2

with open("input.txt") as file:
    text = file.read()

boxes = text.split('\n')

total_feet = 0
for box in boxes:
    l, w, h = map(int, box.split('x'))
    volume = l*w*h
    perimeters = [2*l + 2*w, 2*l + 2*h, 2*w + 2*h]
    smallest_perimeter = min(*perimeters)

    total_feet += volume + smallest_perimeter

print(total_feet)
