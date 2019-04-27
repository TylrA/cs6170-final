from Part1 import Subpart1
from Part1 import Subpart2


def part1():
    repeat_choice = True
    while repeat_choice:

        problem_part_choice = int(input("Please choose a problem subpart\n1. Subpart 1\n2. Subpart 2\n3. Exit\n"))
        while problem_part_choice != 1 and problem_part_choice != 2 and problem_part_choice != 3 and problem_part_choice != 4:
            print("Invalid choice")
            problem_part_choice = int(input("Please choose a problem subpart\n1. Subpart 1\n2. Subpart 2\n3 Exit\n"))

        if problem_part_choice == 1:
            Subpart1.subpart1()
        elif problem_part_choice == 2:
            Subpart2.subpart2()

        repeat = input("Would you like to view another subpart from part 1? y/n\n")
        if repeat != "y":
            repeat_choice = False

