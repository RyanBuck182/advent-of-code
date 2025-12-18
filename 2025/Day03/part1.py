# Part One
# https://adventofcode.com/2025/day/3

with open("input.txt") as file:
    text = file.read()

banks = text.split("\n")

total_joltage = 0
for bank in banks:
    first_battery = max(map(int, bank[:-1]))
    first_battery_index = bank.find(str(first_battery))
    second_battery = max(map(int, bank[first_battery_index+1:]))
    total_joltage += first_battery * 10 + second_battery

print(total_joltage)
