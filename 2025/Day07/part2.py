# Part Two
# https://adventofcode.com/2025/day/7#part2

from collections import defaultdict

with open("input.txt") as file:
    text = file.read()

rows = text.splitlines()

start_position = rows[0].index("S")
beam_positions = {start_position,}
beam_count = defaultdict(int)
beam_count[start_position] = 1
current_row = 0
for row in rows[1:]:
    new_beam_positions = set()
    for beam_pos in beam_positions:
        char = row[beam_pos]
        if char == "^":
            new_beam_positions.add(beam_pos-1)
            new_beam_positions.add(beam_pos+1)
            beam_count[beam_pos+1] += beam_count[beam_pos]
            beam_count[beam_pos-1] += beam_count[beam_pos]
            beam_count[beam_pos] = 0
        else:
            new_beam_positions.add(beam_pos)

    beam_positions = new_beam_positions

total_beams = sum(beam_count.values())
print(total_beams)
