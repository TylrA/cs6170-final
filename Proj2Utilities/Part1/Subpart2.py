import os
from Part1 import Subpart1


def subpart2():
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    Subpart1.display_mds(parent, parent + "/../Data/WassersteinDistances/", "wasserstein_distances")
    Subpart1.display_tsne(parent, parent + "/../Data/WassersteinDistances/", "wasserstein_distances")
