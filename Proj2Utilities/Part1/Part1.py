import os
import scipy.misc
import sys
from subprocess import Popen, PIPE
from Part1 import Subpart1
from Part1 import Subpart2
import random


def part1():
    repeat_choice = True
    while repeat_choice:
        # Begin processing images if not pre-processed.
        print("Checking for image boundaries")
        cwd = os.getcwd()
        parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

        processed_barcodes_path = parent + "/../Data/ImageBarcodes/"
        print("Checking for image barcodes")

        if len(os.listdir(processed_barcodes_path + "dim0/")) == 0:
            print("No barcodes pre-processed")
            construct_barcodes(parent, parent + "/../Data/ImageBoundaries/", parent + "/../Data/ImageBarcodes/")
            print("\nBarcodes constructed")
        else:
            print("Barcodes found")

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


def get_boundary(img):
    row_dim = img.shape[0]
    col_dim = img.shape[1]

    boundary = []
    for i in range(0, row_dim):
        for j in range(0, col_dim):
            pixel_val = img[i, j]

            # The boundary of the physical image is not considered as part of the boundary of the object in the image
            # Begin corner cases
            if i == 0 and j == 0:
                if not img[i + 1, j] == pixel_val or not img[i, j + 1] == pixel_val:
                    boundary.append([i, j])

            elif i == 0 and j == col_dim - 1:
                if not img[i + 1, j] == pixel_val or not img[i, j - 1] == pixel_val:
                    boundary.append([i, j])

            elif i == row_dim - 1 and j == 0:
                if not img[i - 1, j] == pixel_val or not img[i, j + 1] == pixel_val:
                    boundary.append([i, j])

            elif i == row_dim - 1 and j == col_dim - 1:
                if not img[i - 1, j] == pixel_val or not img[i, j - 1] == pixel_val:
                    boundary.append([i, j])

            # Hello Corbin.
            # Begin edge cases.s
            elif i == 0:
                if not img[i + 1, j] == pixel_val or not img[i, j - 1] == pixel_val or not img[i, j + 1] == pixel_val:
                    boundary.append([i, j])

            elif i == row_dim - 1:
                if not img[i - 1, j] == pixel_val or not img[i, j - 1] == pixel_val or not img[i, j + 1] == pixel_val:
                    boundary.append([i, j])

            elif j == 0:
                if not img[i + 1, j] == pixel_val or not img[i - 1, j] == pixel_val or not img[i, j + 1] == pixel_val:
                    boundary.append([i, j])

            elif j == col_dim - 1:
                if not img[i + 1, j] == pixel_val or not img[i - 1, j] == pixel_val or not img[i, j - 1] == pixel_val:
                    boundary.append([i, j])

            # Hello again Corbin.
            # Umm. Begin center case.
            else:
                if not img[i + 1, j] == pixel_val or not img[i - 1, j] == pixel_val \
                        or not img[i, j + 1] == pixel_val or not img[i, j - 1] == pixel_val:
                    boundary.append([i, j])

    return boundary


def process_images(parent, processed_images_path):
    # Get image directories
    max_num_points = 1000
    image_dir = parent + "/../Data/ImageSamples/"
    image_dirs_temp = os.listdir(image_dir)
    image_dirs = []
    for im_dir in image_dirs_temp:
        image_dirs.append(image_dir + im_dir)

    process_image_dirs = []
    for im_dir in image_dirs_temp:
        process_image_dirs.append(im_dir.replace(".gif", ".txt"))

    # Begin processing images
    print("Extracting Boundaries")
    sys.stdout.write('Progress: [%s]' % (' ' * 80))
    for i, im_dir in enumerate(image_dirs):
        img = scipy.misc.imread(im_dir, flatten=True)
        temp_boundary = get_boundary(img)

        # Sample points if more than 5000
        if len(temp_boundary) > max_num_points:
            boundary = random.sample(temp_boundary, max_num_points)
        else:
            boundary = temp_boundary

        with open(processed_images_path + process_image_dirs[i], 'w') as f:
            for entry in boundary:
                print(str(entry[0]) + "," + str(entry[1]), file=f)

        sys.stdout.write('\rProgress: [%s' % ('#' * (i + 1)))
        sys.stdout.write('%s]' % (' ' * (80 - (i + 1))))
        sys.stdout.flush()


def construct_barcodes(parent, image_boundaries_path, barcodes_path):

    image_boundaries_dirs_temp = os.listdir(image_boundaries_path)
    image_boundaries_dirs = []
    for im_dir in image_boundaries_dirs_temp:
        image_boundaries_dirs.append(image_boundaries_path + im_dir)

    image_names = []
    for im_dir in image_boundaries_dirs_temp:
        image_names.append(im_dir.replace(".txt", ""))

    print("Constructing Barcodes")
    sys.stdout.write('Progress: [%s]' % (' ' * 80))
    sys.stdout.flush()
    for i, im_dir in enumerate(image_boundaries_dirs):
        process = Popen([parent + "/../ripser/ripser", im_dir, "--format", "point-cloud"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        lines = (output.decode("utf-8")).split('\n')
        dim0lines = []
        dim1lines = []
        flag0 = False
        flag1 = False
        for line in lines:
            test_line = line.lstrip(' ')
            if line == "":
                continue
            elif test_line == "persistence intervals in dim 0:":
                flag0 = True
                continue
            elif test_line == "persistence intervals in dim 1:":
                flag0 = False
                flag1 = True
                continue

            elif flag0 or flag1:
                l_trim = test_line.lstrip(" [-")
                r_trim = l_trim.rstrip(" -)\n")
                trimmed_line = r_trim.replace(",", " ")

                # Remove barcode with infinite persistence
                if flag0 and len(trimmed_line.strip().split(" ")) > 1:
                    if trimmed_line.strip().split(" ")[1] != "":
                        dim0lines.append(trimmed_line)
                else:
                    dim1lines.append(trimmed_line)

        # Remove duplicate entries
        dim0lines = list(set(dim0lines))
        dim1lines = list(set(dim1lines))

        with open(barcodes_path + "dim0/" + image_names[i] + "dim0.txt", 'w') as f:
            for line in dim0lines:
                print(line, file=f)

        with open(barcodes_path + "dim1/" + image_names[i] + "dim1.txt", 'w') as f:
            for line in dim1lines:
                print(line, file=f)

        sys.stdout.write('\rProgress: [%s' % ('#' * (i + 1)))
        sys.stdout.write('%s]' % (' ' * (80 - (i + 1))))
        sys.stdout.flush()

    # For some reason the dim1 lines print differently. Perhaps this is a bug in ripser?
    image_boundaries_dirs_temp = os.listdir(parent + "/../Data/ImageBarcodes/dim1/")
    image_boundaries_dirs = []
    for im_dir in image_boundaries_dirs_temp:
        image_boundaries_dirs.append(parent + "/../Data/ImageBarcodes/dim1/" + im_dir)
    for im_dir in image_boundaries_dirs:
        lines = []
        with open(im_dir, "r") as f:
            content = f.readlines()
            for i, line in enumerate(content):
                trim_line = line.rstrip("\n")
                temp_line = trim_line.split(" ")
                if trim_line.split(" ")[1] != "":
                    lines.append(trim_line)

        with open(im_dir, "w") as f:
            for line in lines:
                print(line, file=f)
