# Part One
# https://adventofcode.com/2025/day/6

import math

with open("input.txt") as file:
    text = file.read()

str_rows = text.splitlines()  # literally never knew this function existed, would always just do text.split('\n')
rows = []
for row in str_rows:
    rows.append(row.split())

operand_rows = rows[:-1]
operator_row = rows[-1]

# organize operands by col
operand_cols = [[] for _ in range(len(operator_row))]
for row in operand_rows:
    for i in range(len(row)):
        operand_cols[i].append(int(row[i]))

# do the calculations
total_result = 0
for col, operator in zip(operand_cols, operator_row):
    if operator == "+":
        total_result += sum(col)
    elif operator == "*":
        total_result += math.prod(col)

print(total_result)