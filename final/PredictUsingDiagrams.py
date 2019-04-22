from data_structure import critical_point_graph
import os
from sklearn_tda import vector_methods
from sklearn.svm import SVC
import numpy as np
# from scipy.interpolate import splprep, splev
import sys


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


def build_persistence_diagram_from_data(path_to_files, curr_count, max_count):
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
    for i_ in range(0, num_classes_):
        print("\nBuilding diagrams for class %i / %i" % (i_, num_classes_))
        label_abs_dir = main_points_dir + "/" + dirs_by_label[i_]
        simulation_dirs = os.listdir(label_abs_dir)
        simulation_dirs.sort()

        for j in range(0, num_samples_):
            train_labels_.append(dirs_by_label[i_])
            train_diagram = build_persistence_diagram_from_data(label_abs_dir + "/" + simulation_dirs[j], j, len(simulation_dirs))
            train_diagrams_.append(train_diagram)
        for j in range(num_samples_, len(simulation_dirs)):
            test_labels_.append(dirs_by_label[i_])
            test_diagram = build_persistence_diagram_from_data(label_abs_dir + "/" + simulation_dirs[j], j, len(simulation_dirs))
            test_diagrams_.append(test_diagram)

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



def get_diagrams(num_classes, num_training_examples_per_class):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    dim_0_barcode_dirs = os.listdir(parent + "/../Data/ImageBarcodes/dim0/")
    dim_0_barcode_dirs.sort()
    dim_1_barcode_dirs = os.listdir(parent + "/../Data/ImageBarcodes/dim1/")
    dim_1_barcode_dirs.sort()
    labels = []
    for im_dir in dim_0_barcode_dirs:
        labels.append(im_dir.split("-")[0])

    barcodes = []
    dim_0_barcodes = []
    dim_1_barcodes = []
    # min_dim_0 = float('inf')
    # min_dim_1 = float('inf')
    # for bar_dir in dim_0_barcode_dirs:
    #     with open(parent + "/../Data/ImageBarcodes/dim0/" + bar_dir, 'r') as f:
    #         lines = f.readlines()
    #         if len(lines) < min_dim_0:
    #             min_dim_0 = len(lines)
    # for bar_dir in dim_1_barcode_dirs:
    #     with open(parent + "/../Data/ImageBarcodes/dim1/" + bar_dir, 'r') as f:
    #         lines = f.readlines()
    #         if len(lines) < min_dim_1:
    #             min_dim_1 = len(lines)

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