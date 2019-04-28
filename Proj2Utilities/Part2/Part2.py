from Part2 import Subpart1
from Part2 import Subpart2


def part2(crit_or_ripser):

    repeat_choice = True
    while repeat_choice:

        part_choice = int(input("Please choose a problem subpart\n1. Subpart 1\n2. Subpart 2\n3. Exit\n"))
        while part_choice != 1 and part_choice != 2 and part_choice != 3:
            print("Invalid choice")
            part_choice = int(input("Please choose a problem subpart\n1. Subpart 1\n2. Subpart 2\n3. Exit\n"))

        if part_choice == 1:
            Subpart1.subpart1(crit_or_ripser)

        elif part_choice == 2:
            Subpart2.subpart2(crit_or_ripser)
        else:
            exit(0)

        repeat = input("Would you like to view another subpart of Problem 2? y/n\n")
        if repeat != "y":
            repeat_choice = False
