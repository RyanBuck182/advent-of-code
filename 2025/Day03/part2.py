# Part Two
# https://adventofcode.com/2025/day/3#part2

with open("input.txt") as file:
    text = file.read()

banks = text.split("\n")

total_joltage = 0
for bank in banks:
    joltage = 0
    battery_count = len(bank)
    start_index = 0
    for i in range(12):
        battery = max(map(int, bank[start_index:battery_count-11+i]))
        start_index = bank[start_index:].find(str(battery))+1+start_index
        joltage += battery * pow(10, 11-i)

    total_joltage += joltage

print(total_joltage)
