# Part Two
# https://adventofcode.com/2015/day/1#part2

with open("input.txt") as file:
    text = file.read()

pos = 0
solution = 0
for i in range(len(text)):
    if text[i] == "(":
        pos += 1
    elif text[i] == ")":
        pos -= 1

    if pos == -1:
        solution = i + 1
        break

print(solution)
