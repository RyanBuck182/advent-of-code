# Part Two
# https://adventofcode.com/2025/day/5#part2

with open("input.txt") as file:
    text = file.read()

range_text, id_text = text.split("\n\n")
range_strings = range_text.split("\n")
ranges = []
for r in range_strings:
    start, end = r.split("-")
    ranges.append((int(start), int(end)))

# sort ranges by start
ranges.sort(key=lambda r: r[0])

# remove all redundancy
simplified_ranges = []
curr_range = ranges[0]
for next_range in ranges[1:]:
    curr_start, curr_end = curr_range
    next_start, next_end = next_range

    if next_start <= curr_end:
        curr_range = curr_start, max(curr_end, next_end)
    else:
        simplified_ranges.append(curr_range)
        curr_range = next_range
simplified_ranges.append(curr_range)  # append last range

# count ids
total_fresh_ids = 0
for r in simplified_ranges:
    start, end = r
    total_fresh_ids += end - start + 1

print(total_fresh_ids)