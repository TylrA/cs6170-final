from data_structure import critical_point_graph
import os
import numpy as np
# from scipy.interpolate import splprep, splev
import sys


def print_diagram_to_file(gifs, sim, diagram):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    print_path = parent + "/../DataBackup/bubble_backup/ImageBarcodes/"

    with open(print_path + "dim0/" + "gifs%i-sim%i.txt" % (gifs, sim), 'w+') as f:
        for entry in diagram:
            print("%d %d" % (float(entry[0]), float(entry[1])), file=f)
    with open(print_path + "dim1/" + "gifs%i-sim%i.txt" % (gifs, sim), 'w+') as f:
        for entry in diagram:
            print("%d %d" % (float(entry[0]), float(entry[1])), file=f)


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

    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    # Interpolate to non-functional spline
    # Interpolation is currently broken. Until fixed code remains commented
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


def generate_diagrams():
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    main_points_dir = parent + "/smoothed_boundary_points"
    dirs_by_label = os.listdir(main_points_dir)
    dirs_by_label.sort()
    for i_ in range(0, len(dirs_by_label)):
        print("\nBuilding diagrams for class %i / %i" % (i_, len(dirs_by_label)))
        label_abs_dir = main_points_dir + "/" + dirs_by_label[i_]
        simulation_dirs = os.listdir(label_abs_dir)

        for j in range(0, len(simulation_dirs)):
            build_persistence_diagram_from_data(label_abs_dir + "/" + simulation_dirs[j], j, len(simulation_dirs), gifs=i_)


if __name__ == '__main__':
    generate_diagrams()
else:
    exit(-1)