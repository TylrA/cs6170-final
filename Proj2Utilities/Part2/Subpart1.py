from sklearn_tda import kernel_methods
from sklearn.svm import SVC
import os
import random


def subpart1(crit_or_ripser):
    num_classes = int(input("How many image classes would you like to use? 0 - 4\n"))
    num_samples = int(input("How many samples per class would you like? 0 - 10\n"))
    training_labels, training_barcodes, test_labels, test_barcodes = get_diagrams(num_classes, num_samples, crit_or_ripser)

    psk = kernel_methods.PersistenceScaleSpaceKernel()
    psk.fit(training_barcodes)
    train = psk.transform(training_barcodes)
    svc = SVC(kernel='precomputed')
    svc.fit(train, training_labels)

    print("Processing train error")
    train_prediction = svc.predict(train)
    count = 0
    for i in range(0, len(training_labels)):
        if training_labels[i] == train_prediction[i]:
            count += 1

    train_error = 1.0 - (float(count) / float(len(training_labels)))
    print("Train error was %.16f" % train_error)

    print("Processing test error")
    test = psk.transform(test_barcodes)
    test_prediction = svc.predict(test)
    count = 0
    for i in range(0, len(test_labels)):
        if test_labels[i] == test_prediction[i]:
            count += 1

    test_error = 1.0 - (float(count) / float(len(test_labels)))
    print("Test error was %.16f" % test_error)


def get_diagrams(num_classes, num_training_examples_per_class, crit_or_ripser):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    barcodes = []
    labels = []

    dim_0_barcode_dirs = os.listdir(parent + "/../Data/ImageBarcodes/dim0/")
    dim_0_barcode_dirs.sort()
    for im_dir in dim_0_barcode_dirs:
        labels.append(im_dir.split("-")[0])

    dim_0_barcodes = []

    for bar_dir in dim_0_barcode_dirs:
        im_bars = []
        with open(parent + "/../Data/ImageBarcodes/dim0/" + bar_dir, 'r') as f:
            lines = f.readlines()
            for line in lines:
                terms = (line.strip()).split(" ")
                point = [float(terms[0]), float(terms[1])]
                im_bars.append(point)
        # im_bars = random.sample(im_bars, min_dim_0)
        dim_0_barcodes.append(im_bars)

    if crit_or_ripser != "1":
        dim_1_barcode_dirs = os.listdir(parent + "/../Data/ImageBarcodes/dim1/")
        dim_1_barcode_dirs.sort()
        dim_1_barcodes = []

        for bar_dir in dim_1_barcode_dirs:
            with open(parent + "/../Data/ImageBarcodes/dim1/" + bar_dir, 'r') as f:
                im_bars = []
                lines = f.readlines()
                for line in lines:
                    terms = (line.strip()).split(" ")
                    point = [float(terms[0]), float(terms[1])]
                    im_bars.append(point)

            # im_bars = random.sample(im_bars, min_dim_1)
            dim_1_barcodes.append(im_bars)

        for i in range(0, len(dim_0_barcodes)):
            barcodes.append(dim_0_barcodes[i] + dim_1_barcodes[i])

    else:
        for i in range(0, len(dim_0_barcodes)):
            barcodes.append(dim_0_barcodes[i])

    training_barcodes = []
    training_labels = []
    training_indices = []
    for i in range(0, num_classes):
        indices = random.sample(list(range(10 * i, (10 * i + 10))), num_training_examples_per_class)
        indices.sort()
        training_indices += indices
        for index in indices:
            training_barcodes.append(barcodes[index])
            training_labels.append(labels[index])

    test_barcodes = []
    test_labels = []
    for i in range(0, 10 * num_classes):
        if training_indices.count(i) == 0:
            test_barcodes.append(barcodes[i])
            test_labels.append(labels[i])

    return training_labels, training_barcodes, test_labels, test_barcodes
