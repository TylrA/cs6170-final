import os
from subprocess import Popen, PIPE
import sys
import numpy as np
from Part1 import Subpart1


def subpart2():
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    if len(os.listdir(parent + "/../Data/WassersteinDistances/")) == 0:
        
        num_diagrams = len(os.listdir(parent + "/../Data/ImageBoundaries/"))
        progress_max = ((num_diagrams ** 2) / 2) - num_diagrams
        print("Constructing persistence distances using Wasserstein Distance")
        sys.stdout.write('Progress: [%s]' % (' ' * 100))
        sys.stdout.flush()
        dimensional_barcode_dirs = get_dimensional_barcode_dirs(parent)
        for k, barcode_dirs in enumerate(dimensional_barcode_dirs):
            persistance_distances = np.zeros((num_diagrams, num_diagrams))
            current_count = 0
            for i in range(0, num_diagrams):
                for j in range(i + 1, num_diagrams):
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

            print_to_file(persistance_distances.tolist(), parent, k)

    else:
        print("Wasserstein Distance matrix found")

    sys.stdout.write('\n')
    sys.stdout.flush()
    Subpart1.display_mds(parent, parent + "/../Data/WassersteinDistances/", "wasserstein_distances")
    Subpart1.display_tsne(parent, parent + "/../Data/WassersteinDistances/", "wasserstein_distances")

def get_dimensional_barcode_dirs(parent):
    ret = []
    dim0_barcodes_path = parent + "/../Data/ImageBarcodes/dim0/"

    barcodes_dirs_temp = os.listdir(dim0_barcodes_path)
    barcodes_dirs = []
    for bar_dir in barcodes_dirs_temp:
        barcodes_dirs.append(dim0_barcodes_path + bar_dir)

    ret.append(barcodes_dirs)

    dim1_barcodes_path = parent + "/../Data/ImageBarcodes/dim1/"

    barcodes_dirs_temp1 = os.listdir(dim1_barcodes_path)
    barcodes_dirs1 = []
    for bar_dir in barcodes_dirs_temp1:
        barcodes_dirs1.append(dim1_barcodes_path + bar_dir)

    ret.append(barcodes_dirs1)
    return ret


def print_to_file(persistence_distances, parent, k):
    with open(parent + "/../Data/WassersteinDistances/wasserstein_distances" + str(k) + ".txt", 'w') as f:
        for row in persistence_distances:
            string_to_print = ""
            for j, entry in enumerate(row):
                string_to_print += str(entry)
                if j != len(row) - 1:
                    string_to_print += ","

            print(string_to_print, file=f)
