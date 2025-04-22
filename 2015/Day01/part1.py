# Part One
# https://adventofcode.com/2015/day/1

with open("input.txt") as file:
    text = file.read()

ups = text.count("(")
downs = text.count(")")

print(ups - downs)
