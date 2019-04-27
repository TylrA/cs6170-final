import os
from subprocess import Popen, PIPE
import sys
import numpy as np
from matplotlib import pyplot as plt
from sklearn import manifold
from collections import OrderedDict



def subpart1():
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    if len(os.listdir(parent + "/../Data/BottleneckDistances/")) == 0:

        num_diagrams = len(os.listdir(parent + "/../Data/ImageBoundaries/"))
        progress_max = ((num_diagrams ** 2) / 2) - num_diagrams
        print("Constructing persistence distances using Bottleneck Distance")
        sys.stdout.write('Progress: [%s]' % (' ' * 100))
        sys.stdout.flush()
        dimensional_barcode_dirs = get_dimensional_barcode_dirs(parent)
        for k, barcode_dirs in enumerate(dimensional_barcode_dirs):
            persistance_distances = np.zeros((num_diagrams, num_diagrams))
            current_count = 0
            for i in range(0, num_diagrams):
                for j in range(i + 1, num_diagrams):
                    process = Popen([parent + "/../hera/geom_bottleneck/hera_bottleneck_interface",
                                     barcode_dirs[i].strip('\n'), barcode_dirs[j].strip('\n')], stdout=PIPE)
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
        print("Bottleneck Distance matrix found")

    sys.stdout.write('\n')
    sys.stdout.flush()
    display_mds(parent, parent + "/../Data/BottleneckDistances/", "bottleneck_distances")
    display_tsne(parent, parent + "/../Data/BottleneckDistances/", "bottleneck_distances")


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
    with open(parent + "/../Data/BottleneckDistances/bottleneck_distances" + str(k) + ".txt", 'w') as f:
        for row in persistence_distances:
            string_to_print = ""
            for j, entry in enumerate(row):
                string_to_print += str(entry)
                if j != len(row) - 1:
                    string_to_print += ","

            print(string_to_print, file=f)


def display_mds(parent, path, file_name):
    # colormap = {"purple": "bat", "green": "butterfly", "pink": "cattle", "red": "chicken", "teal": "octopus",
    #             "orange": "pocket", "lavender": "ray", "black": "spring"}
    colormap = {"purple": "gifs0", "green": "gifs1", "pink": "gifs2", "red": "gifs3"}

    dim_0_distances = init_from_file(path + file_name + "0.txt")
    dim_1_distances = init_from_file(path + file_name + "1.txt")
    mds0 = manifold.MDS(dissimilarity='precomputed')
    mds1 = manifold.MDS(dissimilarity='precomputed')
    dim_0_mds = mds0.fit_transform(dim_0_distances)
    dim_1_mds = mds1.fit_transform(dim_1_distances)
    dim_0_coloring = get_coloring(parent + "/../Data/ImageBarcodes/dim0/")
    dim_1_coloring = get_coloring(parent + "/../Data/ImageBarcodes/dim1/")
    fig0 = plt.figure()
    ax0 = fig0.add_subplot(111)
    for i, point in enumerate(dim_0_mds[:, 0]):
        ax0.scatter(point, dim_0_mds[i, 1], color=dim_0_coloring[i], lw=0, label=colormap[dim_0_coloring[i]])

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))

    box = ax0.get_position()
    ax0.set_position([box.x0, box.y0, box.width, box.height])

    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Dimension 0 MDS")
    plt.show()

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    for i, point in enumerate(dim_1_mds[:, 0]):
        ax1.scatter(point, dim_1_mds[i, 1], color=dim_1_coloring[i], lw=0, label=colormap[dim_1_coloring[i]])

    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0, box1.width, box1.height])

    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Dimension 1 MDS")
    plt.show()


def display_tsne(parent, path, file_name):
    # colormap = {"purple": "bat", "green": "butterfly", "pink": "cattle", "red": "chicken", "teal": "octopus",
    #             "orange": "pocket", "lavender": "ray", "black": "spring"}
    colormap = {"purple": "gifs0", "green": "gifs1", "pink": "gifs2", "red": "gifs3"}

    dim_0_distances = init_from_file(path + file_name + "0.txt")
    dim_1_distances = init_from_file(path + file_name + "1.txt")
    tsne0 = manifold.TSNE()
    tsne1 = manifold.TSNE()
    dim_0_tsne = tsne0.fit_transform(dim_0_distances)
    dim_1_tsne = tsne1.fit_transform(dim_1_distances)
    dim_0_coloring = get_coloring(parent + "/../Data/ImageBarcodes/dim0/")
    dim_1_coloring = get_coloring(parent + "/../Data/ImageBarcodes/dim1/")
    fig0 = plt.figure()
    ax0 = fig0.add_subplot(111)
    for i, point in enumerate(dim_0_tsne[:, 0]):
        ax0.scatter(point, dim_0_tsne[i, 1], color=dim_0_coloring[i], lw=0, label=colormap[dim_0_coloring[i]])

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))

    box = ax0.get_position()
    ax0.set_position([box.x0, box.y0, box.width, box.height])

    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Dimension 0 t-SNE")
    plt.show()
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    for i, point in enumerate(dim_1_tsne[:, 0]):
        ax1.scatter(point, dim_1_tsne[i, 1], color=dim_1_coloring[i], lw=0, label=colormap[dim_1_coloring[i]])

    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0, box1.width, box1.height])

    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Dimension 1 t-SNE")
    plt.show()


def init_from_file(path):
    persistence_distances = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            terms = line.split(",")
            row = []
            for term in terms:
                row.append(float(term.rstrip('\n')))
            persistence_distances.append(row)

    return np.array(persistence_distances)


def get_coloring(path):
    file_names = os.listdir(path)
    # colormap = {"bat": "purple", "butterfly": "green", "cattle": "pink", "chicken": "red", "octopus": "teal",
    #             "pocket": "orange", "ray": "lavender", "spring": "black"}
    colormap = {"gifs0": "purple", "gifs1": "green", "gifs2": "pink", "gifs3": "red"}
    colors = []
    for file_name in file_names:
        colors.append(colormap[str(file_name).split("-")[0]])

    return colors


# Test coloring for debugging
# def get_coloring(path):
#     string = "bat"
#     colormap = {"bat": "purple", "butterfly": "green", "cattle": "pink", "chicken": "red", "octopus": "teal",
#                 "pocket": "orange", "ray": "lavender", "spring": "black"}
#     colors = []
#     for i in range(0, num_diagrams):
#         if i >= 10:
#             string = "butterfly"
#         if i >= 20:
#             string = "cattle"
#         if i >= 30:
#             string = "chicken"
#         if i >= 40:
#             string = "octopus"
#         if i >= 50:
#             string = "pocket"
#         if i >= 60:
#             string = "ray"
#         if i >= 70:
#             string = "spring"
#
#         colors.append(colormap[string])
#
#     return colors
