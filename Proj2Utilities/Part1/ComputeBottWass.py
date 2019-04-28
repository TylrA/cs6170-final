import os
from subprocess import Popen, PIPE
import sys
import numpy as np


def remove_duplicates(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    lines = list(set(lines))
    with open(file_path, 'w') as f:
        for line in lines:
            temp_line = line.strip()
            print(temp_line, file=f)


def get_dimensional_barcode_dirs(parent_):
    ret = []
    dim0_barcodes_path = parent_ + "/ImageBarcodes/dim0/"

    barcodes_dirs_temp = os.listdir(dim0_barcodes_path)
    barcodes_dirs = []
    for bar_dir in barcodes_dirs_temp:
        barcodes_dirs.append(dim0_barcodes_path + bar_dir)
        remove_duplicates(dim0_barcodes_path + bar_dir)

    ret.append(barcodes_dirs)

    dim1_barcodes_path = parent_ + "/ImageBarcodes/dim1/"

    barcodes_dirs_temp1 = os.listdir(dim1_barcodes_path)
    barcodes_dirs1 = []
    for bar_dir in barcodes_dirs_temp1:
        barcodes_dirs1.append(dim1_barcodes_path + bar_dir)
        remove_duplicates(dim1_barcodes_path + bar_dir)

    ret.append(barcodes_dirs1)
    return ret


def print_to_file(persistence_distances, parent_, k_):
    with open(parent_ + str(k_) + ".txt", 'w') as f:
        for row in persistence_distances:
            string_to_print = ""
            for j_, entry in enumerate(row):
                string_to_print += str(entry)
                if j_ != len(row) - 1:
                    string_to_print += ","

            print(string_to_print, file=f)


def helper(bottleneck, bubble_backup_or_ripser_backup):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    # First compute Bottleneck Distance
    num_diagrams = len(os.listdir(parent + "/../../DataBackup/" + bubble_backup_or_ripser_backup + "/ImageBoundaries/"))
    progress_max = ((num_diagrams ** 2 - num_diagrams) / 2)
    if bottleneck:
        print("Constructing persistence distances using Bottleneck Distance")
    else:
        print("Constructing persistence distances using Wasserstein Distance")

    sys.stdout.write('Progress: [%s]' % (' ' * 100))
    sys.stdout.flush()
    dimensional_barcode_dirs = get_dimensional_barcode_dirs(
        parent + "/../../DataBackup/" + bubble_backup_or_ripser_backup)
    for k, barcode_dirs in enumerate(dimensional_barcode_dirs):
        if k == 1 and bubble_backup_or_ripser_backup == "bubble_backup":
            continue
        persistance_distances = np.zeros((num_diagrams, num_diagrams))
        current_count = 0
        for i in range(0, num_diagrams):
            for j in range(i + 1, num_diagrams):
                if bottleneck:
                    process = Popen([parent + "/../hera/geom_bottleneck/hera_bottleneck_interface",
                                     barcode_dirs[i].strip('\n'), barcode_dirs[j].strip('\n')], stdout=PIPE)
                else:
                    process = Popen([parent + "/../hera/geom_matching/hera_wasserstein_interface",
                                     barcode_dirs[i], barcode_dirs[j]], stdout=PIPE)
                (output, err) = process.communicate()
                exit_code = process.wait()

                persistance_distances[i, j] = float(output)

                current_count += 1
                count = int((current_count * 100) // progress_max)
                sys.stdout.write('\rProgress: [%s' % ('#' * count))
                sys.stdout.write('%s] %s / %i  ' % (' ' * (100 - count), current_count, progress_max))
                sys.stdout.flush()

        for i in range(0, num_diagrams):
            for j in range(i + 1, num_diagrams):
                persistance_distances[j, i] = persistance_distances[i, j]

        if bottleneck:
            print_to_file(persistance_distances.tolist(), parent + "/../../DataBackup/" + bubble_backup_or_ripser_backup + "/BottleneckDistances/bottleneck_distances", k)
        else:
            print_to_file(persistance_distances.tolist(), parent + "/../../DataBackup/" + bubble_backup_or_ripser_backup + "/WassersteinDistances/bottleneck_distances", k)

    sys.stdout.write('\n')
    sys.stdout.flush()


if __name__ == '__main__':

    bubble_backup_or_ripser_backup = sys.argv[1]
    helper(bottleneck=True, bubble_backup_or_ripser_backup=bubble_backup_or_ripser_backup)
    helper(bottleneck=False, bubble_backup_or_ripser_backup=bubble_backup_or_ripser_backup)

else:
    exit(-1)
