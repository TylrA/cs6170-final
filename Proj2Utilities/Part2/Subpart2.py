from sklearn_tda import vector_methods
from Part2 import Subpart1
from sklearn.svm import SVC
import numpy as np


def run_tests(bandwidths_list, kernel, training_labels_, training_diagrams_, testing_labels_, testing_diagrams_):
    for bandwidth in bandwidths_list:
        print("Using %.2f Bandwidth" % bandwidth)
        psk = vector_methods.PersistenceImage(bandwidth=bandwidth, resolution=[100, 100])

        psk.fit(np.array(training_diagrams_))
        train = psk.transform(np.array(training_diagrams_))
        if kernel is None:
            svc = SVC(gamma='scale')
        else:
            svc = SVC(gamma='scale', kernel=kernel)

        train_error = svc.fit(train, training_labels_).score(train, training_labels_)

        print("Train error was %.16f" % (1.0 - train_error))

        psk.fit(testing_diagrams_)
        test = psk.transform(testing_diagrams_)
        test_error = svc.score(test, testing_labels_)
        print("Test error was %.16f\n" % (1.0 - test_error))


def subpart2():
    num_classes = int(input("How many image classes would you like to use? 0 - 4\n"))
    num_samples = int(input("How many samples per class would you like? 0 - 10\n"))
    training_labels, training_barcodes, test_labels, test_barcodes = Subpart1.get_diagrams(num_classes, num_samples)

    training_diagrams = []
    for i in range(0, len(training_barcodes)):
        training_diagrams.append(np.array(training_barcodes[i]))

    testing_diagrams = []
    for i in range(0, len(test_barcodes)):
        testing_diagrams.append(np.array(test_barcodes[i]))

    bandwidths = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]

    # Default Kernel
    print("\nUsing default RBF Kernel\n")
    run_tests(bandwidths, None, training_labels, training_barcodes, test_labels, test_barcodes)

    # Linear Kernel
    print("\nUsing Linear Kernel\n")
    run_tests(bandwidths, 'linear', training_labels, training_barcodes, test_labels, test_barcodes)

    # Polynomial Kernel
    print("\nUsing Cubic Polynomial Kernel\n")
    run_tests(bandwidths, 'poly', training_labels, training_barcodes, test_labels, test_barcodes)

    # Sigmoid Kernel
    print("\nUsing Sigmoid Kernel\n")
    run_tests(bandwidths, 'sigmoid', training_labels, training_barcodes, test_labels, test_barcodes)
