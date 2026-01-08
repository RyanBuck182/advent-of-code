# Part Two
# https://adventofcode.com/2025/day/6#part2

import math

with open("input.txt") as file:
    text = file.read()

rows = text.splitlines()

# use spaces to pad all rows to the same length
row_length = max(len(row) for row in rows)
padded_rows = [row.ljust(row_length) for row in rows]

# separate operands and operators
operand_rows = padded_rows[:-1]
operator_row = padded_rows[-1].split()

# create operands by combining a character from each row
operands = ["" for _ in range(row_length)]
for row in operand_rows:
    for i in range(len(row)):
        operands[i] += row[i]
operands = map(lambda o: o.strip(), operands)


# group operands by column
column_count = len(operator_row)
columns = [[] for _ in range(column_count)]
current_col = 0
for operand in operands:
    if operand != "":
        columns[current_col].append(operand)
    else:
        current_col += 1

# convert str to int
columns = [map(int, col) for col in columns]

# calculate result
total_result = 0
for col, operator in zip(columns, operator_row):
    if operator == "+":
        total_result += sum(col)
    elif operator == "*":
        total_result += math.prod(col)

print(total_result)