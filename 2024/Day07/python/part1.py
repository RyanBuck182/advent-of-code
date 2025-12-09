# Part One
# https://adventofcode.com/2024/day/7

with open("input.txt") as file:
    text = file.read()

operations = [lambda x, y: x + y, lambda x, y: x * y]
equations = text.split("\n")

total_calibration_result = 0
for equation in equations:
    parts = equation.split(" ")
    test_value = int(parts[0][:-1])
    terms = [int(term) for term in parts[1:]]

    def test_equation(current_total: int = terms[0], term_index: int = 1) -> bool:
        if term_index == len(terms):
            return current_total == test_value
        else:
            valid = False
            for operation in operations:
                result = operation(current_total, terms[term_index])
                if test_equation(result, term_index + 1):
                    valid = True
                    break
            return valid

    if test_equation():
        total_calibration_result += test_value

print(total_calibration_result)
