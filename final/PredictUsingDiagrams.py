from data_structure import critical_point_graph
import os
from sklearn_tda import vector_methods
from sklearn.svm import SVC
import numpy as np
# from scipy.interpolate import splprep, splev
import sys
import random


def print_diagram_to_file(gifs, sim, diagram):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    print_path = parent + "/diagrams/"

    with open (print_path + "gifs%i-sim%i.txt" % (gifs, sim), 'w') as f:
        for entry in diagram:
            print("[%d,%d)" % (float(entry[0]), float(entry[1])), file=f)



def get_critical_points_from_file(path, time):
    # Read points
    x_coords = []
    y_coords = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            temp_line = line .strip('\n')
            x_coords.append(float(temp_line.split(' ')[0]))
            y_coords.append(float(temp_line.split(' ')[1]))

    # Interpolate to non-functional spli)ne
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    # Interpolation is currently broken. If fixing is desired, code remains commented
    # tck, u= splprep(x=[x_coords, y_coords],  w=None)
    # new_points = splev(u, tck)
    # x_coords = new_points[0]
    # y_coords = new_points[1]

    diff_x = np.diff(x_coords, n=1, axis=0)
    diff_y = np.diff(y_coords, n=1, axis=0)

    critical_points = []

    for i_ in range(1, len(x_coords) - 1):
        for j in range(1, len(y_coords) - 1):
            # check when the difference changes its sign
            if diff_x[i_ - 1] == 0.0:
                diff_x[i_ - 1] = 1e-8
            if diff_x[i_] == 0.0:
                diff_x[i_] = 1e-8
            prev_dydx = diff_y[i_ - 1] / diff_x[i_ - 1]
            next_dydx = diff_y[i_] / diff_x[i_]
            if prev_dydx < 0.0 <= next_dydx:
                critical_points.append(critical_point_graph.CriticalPoint(x_coords[i_], y_coords[i_], 'min', time))
            elif prev_dydx > 0.0 >= next_dydx:
                critical_points.append(critical_point_graph.CriticalPoint(x_coords[i_], y_coords[i_], 'max', time))

    return critical_points


def build_persistence_diagram_from_data(path_to_files, curr_count, max_count, gifs):
    point_files = os.listdir(path_to_files)
    point_files.sort()
    graphs = []
    sys.stdout.write('Progress: [%s]' % (' ' * 100))
    sys.stdout.flush()
    for k, point_file in enumerate(point_files):
        if point_file.split('.')[1] == 'txt':
            count = int(float((k + 1) / len(point_files)) * 100.0)
            critical_points = get_critical_points_from_file(path_to_files + "/" + point_file, k)

            # Build graph for each file and smooth bumps
            graph = critical_point_graph.Graph(k)
            for critical_point in critical_points:
                graph.add_node(critical_point)
            graph.smooth_bumps()

            graphs.append(graph)

            # Update progress
            sys.stdout.write('\rProgress: [%s' % ('#' * count))
            sys.stdout.write('%s] %i / %i ' % (' ' * (100 - count), curr_count, max_count))
            sys.stdout.flush()

    sys.stdout.write('\rProgress: [%s]' % ('#' * 100))
    sys.stdout.flush()

    diagram = critical_point_graph.PersistenceDiagram(graphs, len(point_files))
    diagram.generate_diagram()
    print_diagram_to_file(gifs, curr_count, diagram.diagram)

    # Use the number of data files per simulation as the 'death time'
    return np.array(diagram.diagram)


def generate_diagrams(num_classes_, num_samples_):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    main_points_dir = parent + "/smoothed_boundary_points"
    dirs_by_label = os.listdir(main_points_dir)
    dirs_by_label.sort()
    train_labels_ = []
    train_diagrams_ = []
    test_labels_ = []
    test_diagrams_ = []
    labels_ = []
    diagrams_ = []
    for i_ in range(0, num_classes_):
        print("\nBuilding diagrams for class %i / %i" % (i_, num_classes_))
        label_abs_dir = main_points_dir + "/" + dirs_by_label[i_]
        simulation_dirs = os.listdir(label_abs_dir)
        simulation_dirs.sort()

        # for j in range(0, num_samples_):
        #     train_labels_.append(dirs_by_label[i_])
        #     train_diagram = build_persistence_diagram_from_data(label_abs_dir + "/" + simulation_dirs[j], j, len(simulation_dirs))
        #     train_diagrams_.append(train_diagram)
        # for j in range(num_samples_, len(simulation_dirs)):
        #     test_labels_.append(dirs_by_label[i_])
        #     test_diagram = build_persistence_diagram_from_data(label_abs_dir + "/" + simulation_dirs[j], j, len(simulation_dirs))
        #     test_diagrams_.append(test_diagram)

        for j in range(0, len(simulation_dirs)):
            labels_.append(dirs_by_label[i_])
            train_diagram = build_persistence_diagram_from_data(label_abs_dir + "/" + simulation_dirs[j], j, len(simulation_dirs), gifs=i_)
            diagrams_.append(train_diagram)

        sample_indices = random.sample(range(0, len(simulation_dirs)), num_samples)
        sample_indices.sort()

        for j in range(0, len(simulation_dirs)):
            if j in sample_indices:
                train_diagrams_.append(diagrams_[j])
                train_labels_.append(labels_[j])
            else:
                test_diagrams_.append(diagrams_[j])
                test_labels_.append(labels_[j])

    return train_labels_, train_diagrams_, test_labels_, test_diagrams_


def run_tests(bandwidths_list, kernel, training_labels_, training_diagrams_, testing_labels_, testing_diagrams_, file):
    for bandwidth in bandwidths_list:
        print("Using %.2f Bandwidth" % bandwidth, file=file)
        psk = vector_methods.PersistenceImage(bandwidth=bandwidth, resolution=[100, 100])

        psk.fit(training_diagrams_)
        train = psk.transform(training_diagrams_)
        if kernel is None:
            svc = SVC(gamma='scale')
        else:
            svc = SVC(gamma='scale', kernel=kernel)

        train_error = svc.fit(train, training_labels_).score(train, training_labels_)

        print("Train error was %.16f" % (1.0 - train_error), file=file)

        psk.fit(testing_diagrams_)
        test = psk.transform(testing_diagrams_)
        test_error = svc.score(test, testing_labels_)
        print("Test error was %.16f\n" % (1.0 - test_error), file=file)


if __name__ == '__main__':
    choice = input("Would you like to use Ripser? If no, then the critical point evolution predictor will be run. y/n")
    if choice == 'n':
        num_classes = int(input("How many image classes would you like to use? 2 or 4\n"))
        num_samples = int(input("How many samples per class would you like? 0 - 10\n"))
        training_labels, training_barcodes, test_labels, test_barcodes = generate_diagrams(num_classes, num_samples)

        training_diagrams = []
        for i in range(0, len(training_barcodes)):
            training_diagrams.append(np.array(training_barcodes[i]))

        testing_diagrams = []
        for i in range(0, len(test_barcodes)):
            testing_diagrams.append(np.array(test_barcodes[i]))

        bandwidths = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]

        cwd = os.getcwd()
        parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
        with open(parent + "/diagram_training_results.txt", 'w') as f:

            # Default Kernel
            print("\nUsing default RBF Kernel\n", file=f)
            run_tests(bandwidths, None, training_labels, training_barcodes, test_labels, test_barcodes, f)

            # Linear Kernel
            print("\nUsing Linear Kernel\n", file=f)
            run_tests(bandwidths, 'linear', training_labels, training_barcodes, test_labels, test_barcodes, f)

            # Polynomial Kernel
            print("\nUsing Cubic Polynomial Kernel\n", file=f)
            run_tests(bandwidths, 'poly', training_labels, training_barcodes, test_labels, test_barcodes, f)

            # Sigmoid Kernel
            print("\nUsing Sigmoid Kernel\n", file=f)
            run_tests(bandwidths, 'sigmoid', training_labels, training_barcodes, test_labels, test_barcodes, f)
