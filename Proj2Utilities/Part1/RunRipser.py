import sys
import os
from subprocess import Popen, PIPE


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




if __name__ == '__main__':
    Part1.construct_barcodes()


else:
    exit(-1)