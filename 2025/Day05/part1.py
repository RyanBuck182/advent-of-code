# Part One
# https://adventofcode.com/2025/day/5

with open("input.txt") as file:
    text = file.read()

range_text, id_text = text.split("\n\n")

range_strings = range_text.split("\n")
ranges = []
for r in range_strings:
    start, end = r.split("-")
    ranges.append((int(start), int(end)))

ids = map(int, id_text.split("\n"))

total_fresh = 0
for id in ids:
    for r in ranges:
        start, end = r
        if start <= id <= end:
            total_fresh += 1
            break

print(total_fresh)