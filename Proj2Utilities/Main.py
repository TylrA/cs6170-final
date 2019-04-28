from Part1 import Part1
from Part2 import Part2
import sys


if __name__ == "__main__":
    repeat_choice = True
    while repeat_choice:

        part_choice = int(input("\nPlease choose a part of Project 2 to view.\n1. Part 1\n2. Part 2\n3. Exit\n"))
        while part_choice != 1 and part_choice != 2 and part_choice != 3:
            print("Invalid choice")
            part_choice = int(input("Please choose a part of Project 2 to view.\n1. Part 1\n2. Part 2\n3. Exit\n"))

        if part_choice == 1:
            Part1.part1(sys.argv[1])

        elif part_choice == 2:
            Part2.part2(sys.argv[1])
        else:
            exit(0)

        repeat = input("Would you like to view another part of Project 2? y/n\n")
        if repeat != "y":
            repeat_choice = False

else:
    exit(-1)
