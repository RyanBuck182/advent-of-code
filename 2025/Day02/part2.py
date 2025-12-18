# Part Two
# https://adventofcode.com/2025/day/2#part2

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
        digit_count = get_digit_count(num)

        invalid_id = False
        for digits_per_part in range(1, (digit_count // 2) + 1):
            if digit_count % digits_per_part != 0:
                continue

            part_count = digit_count // digits_per_part
            lowest_part = num % pow(10, digits_per_part)

            test_num = num
            for part_num in range(part_count):
                test_num -= lowest_part * pow(10, part_num * digits_per_part)

            if test_num == 0:
                invalid_id = True
                break

        if invalid_id:
            id_sum += num

print(id_sum)
