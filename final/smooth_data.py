import numpy as np
import sys
import os

# This  may actually be non-useful. I don't recall if this works on non-functional datasets

def denoise_using_reg_ls(sample, lambd):
    dim = sample.shape[0]
    iden = np.identity(dim)
    L = np.zeros((dim - 1, dim))
    for i in range(0, dim - 1):
        L[i, i] = 1
        L[i, i + 1] = -1

    return np.linalg.inv(iden + lambd * (L.transpose()).dot(L)).dot(sample)


# Main takes 1 command line argument, a float 'lambd' that corresponds to the hyperparameter
# of regularized least squares. Suggested range of lambd is [0.0, 100]. 0.0 corresponds to
# no smoothing and the larger the value of lambd the more smooth the regularization. Keep in
# mind that too high of a value for 'lambd' will lead to decreased accuracy of the interpolated
# data.
if __name__ == '__main__':
    lambd = float(sys.argv[1])
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))
    boundary_file_names = os.listdir(parent + "/boundary_points")
    for file_name in boundary_file_names:
        x = []
        with open(parent + "/boundary_points/" + file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                terms = line.split(',')
                point = []
                for term in terms:
                    point.append(float(term))
                x.append(point)

        regularized_x = denoise_using_reg_ls(np.array(x), lambd)
        with open(parent + "/smoothed_boundary_points/" + file_name, 'w') as f:
            print_x = regularized_x.tolist()
            for point in print_x:
                for i, term in enumerate(point):
                    if i == len(point) - 1:
                        print(str(term), f)
                    else:
                        print(str(term) + ',', f)