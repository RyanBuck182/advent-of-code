# Part One
# https://adventofcode.com/2025/day/2

with open("input.txt") as file:
    text = file.read()


def get_digit_count(num):
    digits = 0
    while num != 0:
        num //= 10
        digits += 1

    return digits


ranges = text.split(",")
ranges = [r.split("-") for r in ranges]

id_sum = 0
for r in ranges:
    range_start = int(r[0])
    range_end = int(r[1])

    for num in range(range_start, range_end + 1):
        digits = get_digit_count(num)
        if digits % 2 != 0:
            continue

        upper_half = num // pow(10, digits / 2)
        lower_half = num % pow(10, digits / 2)
        if upper_half != lower_half:
            continue

        id_sum += num

print(id_sum)
