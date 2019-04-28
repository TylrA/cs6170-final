import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn import manifold
from collections import OrderedDict


def subpart1(crit_or_ripser):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    display_mds(parent, parent + "/../Data/BottleneckDistances/", "bottleneck_distances", crit_or_ripser, "Bottleneck")
    display_tsne(parent, parent + "/../Data/BottleneckDistances/", "bottleneck_distances", crit_or_ripser, "Bottleneck")


def display_mds(parent, path, file_name, crit_or_ripser, pers_type):
    colormap = {"purple": "(1.0, 0.0)", "green": "(0.8, 0.0)", "pink": "(1.0, 0.2)", "red": "(0.8, 0.2)"}

    dim_0_distances = init_from_file(path + file_name + "0.txt")
    mds0 = manifold.MDS(dissimilarity='precomputed')
    dim_0_mds = mds0.fit_transform(dim_0_distances)
    dim_0_coloring = get_coloring(parent + "/../Data/ImageBarcodes/dim0/")
    if crit_or_ripser != "1":
        dim_1_distances = init_from_file(path + file_name + "1.txt")
        mds1 = manifold.MDS(dissimilarity='precomputed')
        dim_1_mds = mds1.fit_transform(dim_1_distances)
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
    if crit_or_ripser == "1":
        plt.title("Critical Diagram " + pers_type + " MDS")
    else:
        plt.title("Dimension 0 " + pers_type + " MDS")
    plt.show()

    if crit_or_ripser != "1":
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        for i, point in enumerate(dim_1_mds[:, 0]):
            ax1.scatter(point, dim_1_mds[i, 1], color=dim_1_coloring[i], lw=0, label=colormap[dim_1_coloring[i]])

        box1 = ax1.get_position()
        ax1.set_position([box1.x0, box1.y0, box1.width, box1.height])

        plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title("Dimension 1 " + pers_type + " MDS")
        plt.show()


def display_tsne(parent, path, file_name, crit_or_ripser, pers_type):
    colormap = {"purple": "(1.0, 0.0)", "green": "(0.8, 0.0)", "pink": "(1.0, 0.2)", "red": "(0.8, 0.2)"}

    dim_0_distances = init_from_file(path + file_name + "0.txt")
    tsne0 = manifold.TSNE()
    dim_0_tsne = tsne0.fit_transform(dim_0_distances)
    dim_0_coloring = get_coloring(parent + "/../Data/ImageBarcodes/dim0/")
    if crit_or_ripser != "1":
        dim_1_distances = init_from_file(path + file_name + "1.txt")
        tsne1 = manifold.TSNE()
        dim_1_tsne = tsne1.fit_transform(dim_1_distances)
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
    if crit_or_ripser != "1":
        plt.title("Dimension 0 " + pers_type + " t-SNE")
    else:
        plt.title("Critical Diagram " + pers_type + " t-SNE")
    plt.show()

    if crit_or_ripser != "1":
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        for i, point in enumerate(dim_1_tsne[:, 0]):
            ax1.scatter(point, dim_1_tsne[i, 1], color=dim_1_coloring[i], lw=0, label=colormap[dim_1_coloring[i]])

        box1 = ax1.get_position()
        ax1.set_position([box1.x0, box1.y0, box1.width, box1.height])

        plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title("Dimension 1 " + pers_type + " t-SNE")
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
    colormap = {"(1.0, 0.0)": "purple", "(0.8, 0.0)": "green", "(1.0, 0.2)": "pink", "(0.8, 0.2)": "red"}
    namemap = {"gifs0": "(1.0, 0.0)", "gifs1": "(0.8, 0.0)", "gifs2": "(1.0, 0.2)", "gifs3": "(0.8, 0.2)"}
    colors = []
    for file_name in file_names:
        colors.append(colormap[namemap[str(file_name).split("-")[0]]])

    return colors
