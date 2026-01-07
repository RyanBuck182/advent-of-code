# Part Two
# https://adventofcode.com/2025/day/4#part2

with open("input.txt") as file:
    text = file.read()

paper = text.replace("@", "1")
paper = paper.replace(".", "0")
paper = paper.replace("\n", "")
paper = list(map(int, paper))


def check_paper(index):
    if 0 <= index < len(paper):
        return paper[index]
    return 0


def remove_paper():
    removed_paper = 0
    for i in range(len(paper)):
        # not a roll of paper, skip
        if paper[i] == 0:
            continue

        adj_paper_count = 0

        adj_paper_count += check_paper(i - 139)  # top
        adj_paper_count += check_paper(i + 139)  # bottom

        # shouldn't check to the left if it's on the left edge
        if i % 139 != 0:
            adj_paper_count += check_paper(i - 140)  # top left
            adj_paper_count += check_paper(i - 1)    # left
            adj_paper_count += check_paper(i + 138)  # bottom left

        # shouldn't check to the right if it's on the right edge
        if (i + 1) % 139 != 0:
            adj_paper_count += check_paper(i - 138)  # top right
            adj_paper_count += check_paper(i + 1)    # right
            adj_paper_count += check_paper(i + 140)  # bottom right

        if adj_paper_count < 4:
            removed_paper += 1
            paper[i] = 0

    return removed_paper


total_removed_paper = 0
paperWasRemoved = True
while paperWasRemoved:
    removed_paper = remove_paper()
    total_removed_paper += removed_paper
    if removed_paper == 0:
        paperWasRemoved = False

print(total_removed_paper)
