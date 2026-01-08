# Part One
# https://adventofcode.com/2025/day/7

with open("input.txt") as file:
    text = file.read()

rows = text.splitlines()

start_position = rows[0].index("S")
beam_positions = {start_position,}
splits = 0
current_row = 0
for row in rows[1:]:
    new_beam_positions = set()
    for beam_pos in beam_positions:
        char = row[beam_pos]
        if char == "^":
            new_beam_positions.add(beam_pos-1)
            new_beam_positions.add(beam_pos+1)
            splits += 1
        else:
            new_beam_positions.add(beam_pos)

    beam_positions = new_beam_positions

print(splits)
