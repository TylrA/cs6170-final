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
    sys.stdout.write('Progress: [%s]' % (' ' * len(image_boundaries_dirs)))
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
            test_line = line.strip()
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
                # Ignore barcode with infinite persistence
                if ", )" not in test_line:
                    l_trim = test_line.lstrip("[-")
                    r_trim = l_trim.rstrip("-)\n")
                    trimmed_line = r_trim.replace(",", " ")
                    if flag0:
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
        sys.stdout.write('%s]' % (' ' * (len(image_boundaries_dirs) - (i + 1))))
        sys.stdout.flush()


if __name__ == '__main__':
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    construct_barcodes(parent=parent, image_boundaries_path=parent + "../../DataBackup/ripser_backup/ImageBoundaries/",
                       barcodes_path="../../DataBackup/ripser_backup/ImageBarcodes/")
    sys.stdout.write('\n')
    sys.stdout.flush()

else:
    exit(-1)
